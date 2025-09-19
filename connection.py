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
        
        if not hasattr(SerialTransport, '_thread_counter'):
            SerialTransport._thread_counter = 0
            SerialTransport._thread_map = {}

        # Log version info during initialization
        try:
            from makcu import __version__
            version = __version__
            self._log(f"Makcu version: {version}")
        except ImportError:
            self._log("Makcu version info not available")
        
        self._log(f"Initializing SerialTransport with params: fallback='{fallback}', debug={debug}, send_init={send_init}, auto_reconnect={auto_reconnect}, override_port={override_port}")

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
                

        self._ascii_decode_table = bytes(range(128))
        
        self._log("SerialTransport initialization completed")


    def _log(self, message: str, level: str = "INFO") -> None:
        if not self.debug:
            return
            
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        thread_id = threading.get_ident()
        
        # Map thread ID to a simple number
        if thread_id not in SerialTransport._thread_map:
            SerialTransport._thread_counter += 1
            SerialTransport._thread_map[thread_id] = SerialTransport._thread_counter
        
        thread_num = SerialTransport._thread_map[thread_id]
        entry = f"[{timestamp}] [T:{thread_num}] [{level}] {message}"
        print(entry, flush=True)

    def _generate_command_id(self) -> int:
        old_counter = self._command_counter
        self._command_counter = (self._command_counter + 1) & 0x2710
        return self._command_counter

    def find_com_port(self) -> Optional[str]:
        self._log("Starting COM port discovery")
        
        if self.override_port:
            self._log(f"Override port enabled, using: {self._fallback_com_port}")
            return self._fallback_com_port
            
        all_ports = list_ports.comports()
        self._log(f"Found {len(all_ports)} COM ports total")

        target_hwid = "VID:PID=1A86:55D3"
        
        for i, port in enumerate(all_ports):
            self._log(f"Port {i}: {port.device} - HWID: {port.hwid}")
            if target_hwid in port.hwid.upper():
                self._log(f"Target device found on port: {port.device}")
                return port.device
        
        self._log("Target device not found in COM port scan")
        
        if self._fallback_com_port:
            self._log(f"Using fallback COM port: {self._fallback_com_port}")
            return self._fallback_com_port
        
        self._log("No fallback port specified, returning None")
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
        print("\n", end='')
        self._log(f"Button state changed: 0x{self._last_button_mask:02X} -> 0x{byte_val:02X}")

        for bit in range(8):
            if changed_bits & (1 << bit):
                is_pressed = bool(byte_val & (1 << bit))
                button_name = self.BUTTON_MAP[bit] if bit < len(self.BUTTON_MAP) else f"bit{bit}"
            
                self._log(f"Button {button_name}: {'PRESSED' if is_pressed else 'RELEASED'}")
                print(">>> ", end='', flush=True)
                if is_pressed:
                    self._button_states |= (1 << bit)
                else:
                    self._button_states &= ~(1 << bit)
            
                if self._button_callback and bit < len(self.BUTTON_ENUM_MAP):
                    try:
                        self._button_callback(self.BUTTON_ENUM_MAP[bit], is_pressed)
                    except Exception as e:
                        self._log(f"Button callback failed: {e}", "ERROR")

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
                age = current_time - pending.timestamp
                self._log(f"Command '{pending.command}' timed out after {age:.3f}s", "ERROR")
                del self._pending_commands[cmd_id]
                if not pending.future.done():
                    pending.future.set_exception(
                        MakcuTimeoutError(f"Command #{cmd_id} timed out")
                    )

    def _listen(self) -> None:
        self._log("Starting listener thread")
        read_buffer = bytearray(4096)
        line_buffer = bytearray(256)
        line_pos = 0

        serial_read = self.serial.read
        serial_in_waiting = lambda: self.serial.in_waiting
        is_connected = lambda: self._is_connected
        stop_requested = self._stop_event.is_set

        last_cleanup = time.time()
        cleanup_interval = 0.05
        
        expecting_text_mode = False
        last_byte = None

        while is_connected() and not stop_requested():
            try:
                bytes_available = serial_in_waiting()
                if not bytes_available:
                    time.sleep(0.001)
                    continue
            
                bytes_read = serial_read(min(bytes_available, 4096))
                for byte_val in bytes_read:
                    
                    if last_byte == 0x0D and byte_val == 0x0A:
                        if line_pos > 0:
                            line = bytes(line_buffer[:line_pos])
                            line_pos = 0
                            if line:
                                response = self._parse_response_line(line)
                                if response.content:
                                    self._process_pending_commands(response.content)
                        expecting_text_mode = False
                    
                    elif byte_val >= 32 or byte_val in (0x09,):
                        expecting_text_mode = True
                        if line_pos < 256:
                            line_buffer[line_pos] = byte_val
                            line_pos += 1
                    
                    elif byte_val == 0x0D:
                        if expecting_text_mode or line_pos > 0:
                            expecting_text_mode = True
                        else:
                            pass
                    
                    elif byte_val == 0x0A:
                        last_byte_str = f"0x{last_byte:02X}" if last_byte is not None else "None"
                        # self._log(f"LF detected: last_byte={last_byte_str}, expecting_text={expecting_text_mode}, line_pos={line_pos}", "DEBUG")
                        
                        button_combination_detected = False
                        
                        if (self._last_button_mask != 0 or 
                            (last_byte is not None and last_byte < 32 and last_byte != 0x0D) or
                            (line_pos > 0 and not expecting_text_mode)):
                            
                            # self._log("LF: Detected as button combination (right + mouse4 = 0x0A)", "DEBUG")
                            self._handle_button_data(byte_val)
                            expecting_text_mode = False
                            button_combination_detected = True
                            line_pos = 0
                        
                        if not button_combination_detected:
                            if last_byte == 0x0D:
                                self._log("LF: Completing CRLF sequence", "DEBUG")
                                if line_pos > 0:
                                    line = bytes(line_buffer[:line_pos])
                                    line_pos = 0
                                    if line:
                                        response = self._parse_response_line(line)
                                        if response.content:
                                            self._process_pending_commands(response.content)
                                expecting_text_mode = False
                            elif line_pos > 0 and expecting_text_mode:
                                self._log("LF: Ending line with text in buffer", "DEBUG")
                                line = bytes(line_buffer[:line_pos])
                                line_pos = 0
                                if line:
                                    response = self._parse_response_line(line)
                                    if response.content:
                                        self._process_pending_commands(response.content)
                                expecting_text_mode = False
                            elif expecting_text_mode:
                                self._log("LF: Empty line in text mode", "DEBUG")
                                expecting_text_mode = False
                            else:
                                self._log("LF: Treating as button data (no text context)", "DEBUG")
                                self._handle_button_data(byte_val)
                                expecting_text_mode = False
                                line_pos = 0  # Clear any accumulated data
                    
                    elif byte_val < 32:
                        if last_byte == 0x0D:
                            self._log(f"Processing delayed CR as button data: 0x0D", "DEBUG")
                            self._handle_button_data(0x0D)
                        
                        self._handle_button_data(byte_val)
                        expecting_text_mode = False
                        line_pos = 0
                    
                    last_byte = byte_val
                            
                current_time = time.time()
                if current_time - last_cleanup > cleanup_interval:
                    self._cleanup_timed_out_commands()
                    last_cleanup = current_time
                
            except serial.SerialException as e:
                self._log(f"Serial exception in listener: {e}", "ERROR")
                if self.auto_reconnect:
                    self._attempt_reconnect()
                else:
                    break
            except Exception as e:
                self._log(f"Unexpected exception in listener: {e}", "ERROR")

        self._log("Listener thread ending")

    def _attempt_reconnect(self) -> None:
        self._log(f"Attempting reconnect #{self._reconnect_attempts + 1}/{self.MAX_RECONNECT_ATTEMPTS}")
        
        if self._reconnect_attempts >= self.MAX_RECONNECT_ATTEMPTS:
            self._log("Max reconnect attempts reached, giving up", "ERROR")
            self._is_connected = False
            return
        
        self._reconnect_attempts += 1
        
        try:
            if self.serial and self.serial.is_open:
                self._log("Closing existing serial connection for reconnect")
                self.serial.close()
            
            time.sleep(self.RECONNECT_DELAY)
            
            self.port = self.find_com_port()
            if not self.port:
                raise MakcuConnectionError("Device not found during reconnect")
            
            self._log(f"Reconnecting to {self.port} at {self.baudrate} baud")
            self.serial = serial.Serial(
                self.port, 
                self.baudrate, 
                timeout=0.001,
                write_timeout=0.01
            )
            
            if not self._change_baud_to_4M():
                raise MakcuConnectionError("Failed to change baud during reconnect")
            
            if self.send_init:
                self._log("Sending init command during reconnect")
                self.serial.write(b"km.buttons(1)\r")
                self.serial.flush()
            
            self._reconnect_attempts = 0
            self._log("Reconnect successful")
            
        except Exception as e:
            self._log(f"Reconnect attempt failed: {e}", "ERROR")
            time.sleep(self.RECONNECT_DELAY)

    def _change_baud_to_4M(self) -> bool:
        self._log("Changing baud rate to 4M")
        
        if self.serial and self.serial.is_open:
            self.serial.write(self.BAUD_CHANGE_COMMAND)
            self.serial.flush()
            
            time.sleep(0.02)
            
            old_baud = self.serial.baudrate
            self.serial.baudrate = 4000000
            self._current_baud = 4000000
            
            self._log(f"Baud rate changed: {old_baud} -> {self.serial.baudrate}")
            return True
        
        self._log("Cannot change baud - serial not open", "ERROR")
        return False

    def connect(self) -> None:
        connection_start = time.time()
        self._log("Starting connection process")
        
        if self._is_connected:
            self._log("Already connected")
            return
        
        if not self.override_port:
            self.port = self.find_com_port()
        else:
            self.port = self._fallback_com_port
            
        if not self.port:
            raise MakcuConnectionError("Makcu device not found")
        
        self._log(f"Connecting to {self.port}")
        
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
            
            connection_time = time.time() - connection_start
            self._log(f"Connection established in {connection_time:.3f}s")
            
            if self.send_init:
                self._log("Sending initialization command")
                init_cmd = b"km.buttons(1)\r"
                self.serial.write(init_cmd)
                self.serial.flush()

            self._stop_event.clear()
            self._listener_thread = threading.Thread(
                target=self._listen, 
                daemon=True,
                name="MakcuListener"
            )
            self._listener_thread.start()
            self._log(f"Listener thread started: {self._listener_thread.name}")
            
        except Exception as e:
            self._log(f"Connection failed: {e}", "ERROR")
            if self.serial:
                try:
                    self.serial.close()
                except:
                    pass
            raise MakcuConnectionError(f"Failed to connect: {e}")

    def disconnect(self) -> None:
        self._log("Starting disconnection process")
        
        self._is_connected = False
        
        if self.send_init:
            self._stop_event.set()
            if self._listener_thread and self._listener_thread.is_alive():
                self._listener_thread.join(timeout=0.1)
                if self._listener_thread.is_alive():
                    self._log("Listener thread did not join within timeout")
                else:
                    self._log("Listener thread stopped")
        
        pending_count = len(self._pending_commands)
        if pending_count > 0:
            self._log(f"Cancelling {pending_count} pending commands")
        
        with self._command_lock:
            for cmd_id, pending in self._pending_commands.items():
                if not pending.future.done():
                    pending.future.cancel()
            self._pending_commands.clear()
        
        if self.serial and self.serial.is_open:
            self._log(f"Closing serial port: {self.serial.port}")
            self.serial.close()
            
        self.serial = None
        self._log("Disconnection completed")

    def send_command(self, command: str, expect_response: bool = False, 
                timeout: float = DEFAULT_TIMEOUT) -> Optional[str]:
        command_start = time.time()
        
        if not self._is_connected or not self.serial or not self.serial.is_open:
            raise MakcuConnectionError("Not connected")
        
        if not expect_response:
            self.serial.write(f"{command}\r\n".encode('ascii'))
            self.serial.flush()
            send_time = time.time() - command_start
            self._log(f"Command '{command}' sent in {send_time:.5f}s (no response expected)")
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
            cmd_bytes = f"{tagged_command}\r\n".encode('ascii')
            self.serial.write(cmd_bytes)
            self.serial.flush()
            
            result = future.result(timeout=timeout)
            
            response = result.split('#')[0] if '#' in result else result
            total_time = time.time() - command_start
            self._log(f"Command '{command}' completed in {total_time:.5f}s total")
            return response
            
        except TimeoutError:
            total_time = time.time() - command_start
            self._log(f"Command '{command}' timed out after {total_time:.3f}s", "ERROR")
            raise MakcuTimeoutError(f"Command timed out: {command}")
        except Exception as e:
            total_time = time.time() - command_start
            self._log(f"Command '{command}' failed after {total_time:.3f}s: {e}", "ERROR")
            with self._command_lock:
                self._pending_commands.pop(cmd_id, None)
            raise

    async def async_send_command(self, command: str, expect_response: bool = False,
                               timeout: float = DEFAULT_TIMEOUT) -> Optional[str]:
        self._log(f"Async sending command: '{command}'")
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None, self.send_command, command, expect_response, timeout
        )

    def is_connected(self) -> bool:
        connected = self._is_connected and self.serial is not None and self.serial.is_open
        return connected

    def set_button_callback(self, callback: Optional[Callable[[MouseButton, bool], None]]) -> None:
        self._log(f"Setting button callback: {callback is not None}")
        self._button_callback = callback

    def get_button_states(self) -> Dict[str, bool]:
        states = {
            self.BUTTON_MAP[i]: bool(self._button_states & (1 << i))
            for i in range(5)
        }
        return states

    def get_button_mask(self) -> int:
        return self._last_button_mask

    def enable_button_monitoring(self, enable: bool = True) -> None:
        cmd = "km.buttons(1)" if enable else "km.buttons(0)"
        self._log(f"{'Enabling' if enable else 'Disabling'} button monitoring")
        self.send_command(cmd)

    async def __aenter__(self):
        self._log("Async context manager enter")
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.connect)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._log("Async context manager exit")
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self.disconnect)

    def __enter__(self):
        self._log("Sync context manager enter")
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._log("Sync context manager exit")
        self.disconnect()