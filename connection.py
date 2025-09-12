import serial
import threading
import time
from typing import Optional, Dict, Callable
from serial.tools import list_ports
from dataclasses import dataclass
from collections import deque
from concurrent.futures import Future
import logging
import asyncio
from .errors import MakcuConnectionError, MakcuTimeoutError
from .enums import MouseButton

logger = logging.getLogger(__name__)

@dataclass
class PendingCommand:
    command_id: int
    command: str
    future: Future
    timestamp: float
    expect_response: bool = True
    timeout: float = 0.1

@dataclass
class ParsedResponse:
    command_id: Optional[int]
    content: str
    is_button_data: bool = False
    button_mask: Optional[int] = None

class SerialTransport:
    
    BAUD_CHANGE_COMMAND = bytearray([0xDE, 0xAD, 0x05, 0x00, 0xA5, 0x00, 0x09, 0x3D, 0x00])
    DEFAULT_TIMEOUT = 0.1
    MAX_RECONNECT_ATTEMPTS = 3
    RECONNECT_DELAY = 0.1
    

    BUTTON_MAP = (
        'left', 'right', 'middle', 'mouse4', 'mouse5'
    )
    
    BUTTON_ENUM_MAP = (
        MouseButton.LEFT,
        MouseButton.RIGHT,
        MouseButton.MIDDLE,
        MouseButton.MOUSE4,
        MouseButton.MOUSE5,
    )

    def __init__(self, fallback: str = "", debug: bool = False, 
                 send_init: bool = True, auto_reconnect: bool = True, 
                 override_port: bool = False) -> None:

        self._fallback_com_port = fallback
        self.debug = debug
        self.send_init = send_init
        self.auto_reconnect = auto_reconnect
        self.override_port = override_port
        

        self._is_connected = False
        self._reconnect_attempts = 0
        self.port: Optional[str] = None
        self.baudrate = 115200
        self.serial: Optional[serial.Serial] = None
        self._current_baud: Optional[int] = None
        

        self._command_counter = 0
        self._pending_commands: Dict[int, PendingCommand] = {}
        self._command_lock = threading.Lock()
        

        self._parse_buffer = bytearray(1024)
        self._buffer_pos = 0
        self._response_queue = deque(maxlen=100)
        

        self._button_callback: Optional[Callable[[MouseButton, bool], None]] = None
        self._last_button_mask = 0
        self._button_states = 0
        

        self._stop_event = threading.Event()
        self._listener_thread: Optional[threading.Thread] = None
        

        self._log_messages: deque = deque(maxlen=100)
        

        self._ascii_decode_table = bytes(range(128))

    def _log(self, message: str, level: str = "INFO") -> None:
        if not self.debug and level == "DEBUG":
            return
            
        if self.debug:

            timestamp = f"{time.time():.3f}"
            entry = f"[{timestamp}] [{level}] {message}"
            self._log_messages.append(entry)
            print(entry, flush=True)

    def _generate_command_id(self) -> int:
        self._command_counter = (self._command_counter + 1) & 0x2710
        return self._command_counter

    def find_com_port(self) -> Optional[str]:
        if self.override_port:
            return self._fallback_com_port
            

        target_hwid = "VID:PID=1A86:55D3"
        
        for port in list_ports.comports():
            if target_hwid in port.hwid.upper():
                self._log(f"Device found: {port.device}")
                return port.device
        
        if self._fallback_com_port:
            self._log(f"Using fallback: {self._fallback_com_port}")
            return self._fallback_com_port
        
        return None

    def _parse_response_line(self, line: bytes) -> ParsedResponse:

        if line.startswith(b'>>> '):
            content = line[4:].decode('ascii', 'ignore').strip()
            return ParsedResponse(None, content, False)
        
        content = line.decode('ascii', 'ignore').strip()
        return ParsedResponse(None, content, False)

    def _handle_button_data(self, byte_val: int) -> None:
        if byte_val == self._last_button_mask:
            return
            
        changed_bits = byte_val ^ self._last_button_mask
        

        for bit in range(5):
            if changed_bits & (1 << bit):
                is_pressed = bool(byte_val & (1 << bit))
                

                if is_pressed:
                    self._button_states |= (1 << bit)
                else:
                    self._button_states &= ~(1 << bit)
                
                if self._button_callback and bit < len(self.BUTTON_ENUM_MAP):
                    try:
                        self._button_callback(self.BUTTON_ENUM_MAP[bit], is_pressed)
                    except Exception:
                        pass
        
        self._last_button_mask = byte_val

    def _process_pending_commands(self, content: str) -> None:
        if not content or not self._pending_commands:
            return

        with self._command_lock:
            if not self._pending_commands:
                return
                

            oldest_id = next(iter(self._pending_commands))
            pending = self._pending_commands[oldest_id]

            if pending.future.done():
                return


            if content == pending.command:
                if not pending.expect_response:
                    pending.future.set_result(pending.command)
                    del self._pending_commands[oldest_id]
            else:
                pending.future.set_result(content)
                del self._pending_commands[oldest_id]

    def _cleanup_timed_out_commands(self) -> None:
        if not self._pending_commands:
            return
            
        current_time = time.time()
        with self._command_lock:

            timed_out = [
                (cmd_id, pending) 
                for cmd_id, pending in self._pending_commands.items()
                if current_time - pending.timestamp > pending.timeout
            ]
            

            for cmd_id, pending in timed_out:
                del self._pending_commands[cmd_id]
                if not pending.future.done():
                    pending.future.set_exception(
                        MakcuTimeoutError(f"Command #{cmd_id} timed out")
                    )


    def _listen(self) -> None:

        read_buffer = bytearray(4096)
        line_buffer = bytearray(256)
        line_pos = 0
        

        serial_read = self.serial.read
        serial_in_waiting = lambda: self.serial.in_waiting
        is_connected = lambda: self._is_connected
        stop_requested = self._stop_event.is_set
        

        last_cleanup = time.time()
        cleanup_interval = 0.05
        
        while is_connected() and not stop_requested():
            try:

                bytes_available = serial_in_waiting()
                if not bytes_available:
                    time.sleep(0.001)
                    continue
                

                bytes_read = serial_read(min(bytes_available, 4096))
                

                for byte_val in bytes_read:

                    if byte_val < 32 and byte_val not in (0x0D, 0x0A):
                        self._handle_button_data(byte_val)
                    else:

                        if byte_val == 0x0A:
                            if line_pos > 0:

                                line = bytes(line_buffer[:line_pos])
                                line_pos = 0
                                
                                if line:
                                    response = self._parse_response_line(line)
                                    if response.content:
                                        self._process_pending_commands(response.content)
                        elif byte_val != 0x0D:
                            if line_pos < 256:
                                line_buffer[line_pos] = byte_val
                                line_pos += 1
                

                current_time = time.time()
                if current_time - last_cleanup > cleanup_interval:
                    self._cleanup_timed_out_commands()
                    last_cleanup = current_time
                    
            except serial.SerialException:
                if self.auto_reconnect:
                    self._attempt_reconnect()
                else:
                    break
            except Exception:
                pass

    def _attempt_reconnect(self) -> None:
        if self._reconnect_attempts >= self.MAX_RECONNECT_ATTEMPTS:
            self._is_connected = False
            return
        
        self._reconnect_attempts += 1
        
        try:
            if self.serial and self.serial.is_open:
                self.serial.close()
            
            time.sleep(self.RECONNECT_DELAY)
            
            self.port = self.find_com_port()
            if not self.port:
                raise MakcuConnectionError("Device not found")
            

            self.serial = serial.Serial(
                self.port, 
                self.baudrate, 
                timeout=0.001,
                write_timeout=0.01
            )
            self._change_baud_to_4M()
            
            if self.send_init:
                self.serial.write(b"km.buttons(1)\r")
                self.serial.flush()
            
            self._reconnect_attempts = 0
            
        except Exception:
            time.sleep(self.RECONNECT_DELAY)

    def _change_baud_to_4M(self) -> bool:
        if self.serial and self.serial.is_open:
            self.serial.write(self.BAUD_CHANGE_COMMAND)
            self.serial.flush()
            time.sleep(0.02)
            self.serial.baudrate = 4000000
            self._current_baud = 4000000
            return True
        return False

    def connect(self) -> None:
        if self._is_connected:
            return
        
        if not self.override_port:
            self.port = self.find_com_port()
        else:
            self.port = self._fallback_com_port
            
        if not self.port:
            raise MakcuConnectionError("Makcu device not found")
        
        try:

            self.serial = serial.Serial(
                self.port, 
                115200, 
                timeout=0.001,
                write_timeout=0.01,
                xonxoff=False,
                rtscts=False,
                dsrdtr=False
            )
            
            if not self._change_baud_to_4M():
                raise MakcuConnectionError("Failed to switch to 4M baud")
            
            self._is_connected = True
            self._reconnect_attempts = 0
            
            if self.send_init:
                self.serial.write(b"km.buttons(1)\r")
                self.serial.flush()
            

            self._stop_event.clear()
            self._listener_thread = threading.Thread(
                target=self._listen, 
                daemon=True,
                name="MakcuListener"
            )
            self._listener_thread.start()
            
        except Exception as e:
            if self.serial:
                self.serial.close()
            raise MakcuConnectionError(f"Failed to connect: {e}")

    def disconnect(self) -> None:
        self._is_connected = False
        
        if self.send_init:
            self._stop_event.set()
            if self._listener_thread and self._listener_thread.is_alive():
                self._listener_thread.join(timeout=0.1)
        
        with self._command_lock:
            for pending in self._pending_commands.values():
                if not pending.future.done():
                    pending.future.cancel()
            self._pending_commands.clear()
        
        if self.serial and self.serial.is_open:
            self.serial.close()
        self.serial = None

    def send_command(self, command: str, expect_response: bool = False, 
                timeout: float = DEFAULT_TIMEOUT) -> Optional[str]:
        if not self._is_connected or not self.serial or not self.serial.is_open:
            raise MakcuConnectionError("Not connected")
        
        if not expect_response:
            self.serial.write(f"{command}\r\n".encode('ascii'))
            self.serial.flush()
            return command
        
        cmd_id = self._generate_command_id()
        tagged_command = f"{command}#{cmd_id}"
        
        future = Future()
        
        with self._command_lock:
            self._pending_commands[cmd_id] = PendingCommand(
                command_id=cmd_id,
                command=command,
                future=future,
                timestamp=time.time(),
                expect_response=expect_response,
                timeout=timeout
            )
        
        try:
            self.serial.write(f"{tagged_command}\r\n".encode('ascii'))
            self.serial.flush()
            
            result = future.result(timeout=timeout)
            return result.split('#')[0] if '#' in result else result
            
        except TimeoutError:
            raise MakcuTimeoutError(f"Command timed out: {command}")
        except Exception as e:
            with self._command_lock:
                self._pending_commands.pop(cmd_id, None)
            raise

    async def async_send_command(self, command: str, expect_response: bool = False,
                               timeout: float = DEFAULT_TIMEOUT) -> Optional[str]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None, self.send_command, command, expect_response, timeout
        )

    def is_connected(self) -> bool:
        return self._is_connected and self.serial is not None and self.serial.is_open

    def set_button_callback(self, callback: Optional[Callable[[MouseButton, bool], None]]) -> None:
        self._button_callback = callback

    def get_button_states(self) -> Dict[str, bool]:
        return {
            self.BUTTON_MAP[i]: bool(self._button_states & (1 << i))
            for i in range(5)
        }

    def get_button_mask(self) -> int:
        return self._last_button_mask

    def enable_button_monitoring(self, enable: bool = True) -> None:
        self.send_command("km.buttons(1)" if enable else "km.buttons(0)")

    async def __aenter__(self):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.connect)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.disconnect)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()