import serial
import threading
import time
from serial.tools import list_ports
from .errors import MakcuConnectionError, MakcuTimeoutError
from .enums import MouseButton

class SerialTransport:
    fallback_com_port = "COM1"
    baud_change_command = bytearray([0xDE, 0xAD, 0x05, 0x00, 0xA5, 0x00, 0x09, 0x3D, 0x00])

    button_map = {
        0: 'left',
        1: 'right',
        2: 'middle',
        3: 'mouse4',
        4: 'mouse5'
    }

    def __init__(self, port=None, debug=False, send_init=True):        
        self._log_messages = []
        self.debug = debug
        self.send_init = send_init
        self._button_callback = None
        self._last_mask = 0
        self._lock = threading.Lock()
        self._is_connected = False
        self._stop_event = threading.Event()
        self._listener_thread = None
        self._button_states = {btn: False for btn in self.button_map.values()}
        self._debounce_time_ms = 50
        self._last_callback_time = {bit: 0 for bit in self.button_map}
        self._pause_listener = False

        self._button_enum_map = {
            0: MouseButton.LEFT,
            1: MouseButton.RIGHT,
            2: MouseButton.MIDDLE,
            3: MouseButton.MOUSE4,
            4: MouseButton.MOUSE5,
        }

        if port:
            self.port = port
        else:
            self.port = self.find_com_port()
            if not self.port:
                raise MakcuConnectionError("Makcu device not found. Please specify a port explicitly.")

        self.baudrate = 115200
        self.serial = None
        self._current_baud = None

    def receive_response(self, max_bytes=1024, max_lines=3, sent_command: str = "") -> str:
        lines = []
        try:
            for _ in range(max_lines):
                line = self.serial.readline(max_bytes)
                if not line:
                    break
                decoded = line.decode(errors="ignore").strip()
                if decoded:
                    lines.append(decoded)
        except Exception as e:
            print(f"[RECV ERROR] {e}")
            return ""

        command_clean = sent_command.strip()
        if lines:
            lines.pop(-1)
        if command_clean in lines and len(lines) > 1:
            lines.remove(command_clean)
        return "\n".join(lines)

    def set_debounce_time(self, ms: int):
        self._debounce_time_ms = ms

    def set_button_callback(self, callback):
        self._button_callback = callback

    def _log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        entry = f"[{timestamp}] {message}"
        self._log_messages.append(entry)
        if len(self._log_messages) > 20:
            self._log_messages.pop(0)
        print(entry, flush=True)

    def find_com_port(self):
        self._log("Searching for CH343 device...")
        for port in list_ports.comports():
            if "USB-Enhanced-SERIAL CH343" in port.description:
                self._log(f"Device found: {port.device}")
                return port.device
        self._log("Device not found.")
        return None

    def _open_serial_port(self, port, baud_rate):
        try:
            self._log(f"Trying to open {port} at {baud_rate} baud.")
            return serial.Serial(port, baud_rate, timeout=0.05)
        except serial.SerialException:
            self._log(f"Failed to open {port} at {baud_rate} baud.")
            return None

    def _change_baud_to_4M(self):
        if self.serial and self.serial.is_open:
            self._log("Sending baud rate switch command to 4M.")
            self.serial.write(self.baud_change_command)
            self.serial.flush()
            port = self.serial.name
            self.serial.close()
            time.sleep(0.1)
            self.serial = self._open_serial_port(port, 4000000)
            if self.serial:
                self._current_baud = 4000000
                self._log("Switched to 4M baud successfully.")
                return True
            else:
                self._log("Failed to reopen port at 4M baud.")
        return False

    def connect(self):
        if self._is_connected:
            self._log("Already connected.")
            return
        self.serial = self._open_serial_port(self.port, 115200)
        if not self.serial:
            raise MakcuConnectionError(f"Failed to connect to {self.port} at 115200.")
        self._log(f"Connected to {self.port} at 115200.")
        if not self._change_baud_to_4M():
            raise MakcuConnectionError("Failed to switch to 4M baud.")
        self._is_connected = True
        if self.send_init:
            with self._lock:
                self.serial.write(b"km.buttons(1)\r")
                self.serial.flush()
                self._log("Sent init command: km.buttons(1)")

            self._stop_event.clear()
            self._listener_thread = threading.Thread(target=self._listen, kwargs={"debug": self.debug}, daemon=True)
            self._listener_thread.start()

    def disconnect(self):
        if self.send_init:
            self._stop_event.set()
            if self._listener_thread:
                self._listener_thread.join()
        with self._lock:
            if self.serial and self.serial.is_open:
                self.serial.close()
            self.serial = None
            self._is_connected = False
            self._log("Disconnected.")

    def is_connected(self):
        return self._is_connected

    def send_command(self, command, expect_response=False):
        time.sleep(0.06)
        if not self._is_connected or not self.serial or not self.serial.is_open:
            raise MakcuConnectionError("Serial connection not open.")
        with self._lock:
            try:
                self._pause_listener = True
                self.serial.reset_input_buffer()
                self.serial.write(command.encode("ascii") + b"\r\n")
                self.serial.flush()
                if expect_response:
                    response = self.receive_response(sent_command=command)
                    if not response:
                        raise MakcuTimeoutError(f"No response from device for command: {command}")
                    return response
            finally:
                self._pause_listener = False

    def get_button_states(self):
        return dict(self._button_states)

    def get_button_mask(self) -> int:
        mask = 0
        for i, name in self.button_map.items():
            if self._button_states.get(name, False):
                mask |= (1 << i)
        return mask

    def enable_button_monitoring(self, enable: bool = True):
        self.send_command("km.buttons(1)" if enable else "km.buttons(0)")

    def catch_button(self, button: str):
        command = {
            "LEFT": "km.catch_ml(0)",
            "RIGHT": "km.catch_mr(0)",
            "MIDDLE": "km.catch_mm(0)",
            "MOUSE4": "km.catch_ms1(0)",
            "MOUSE5": "km.catch_ms2(0)",
        }.get(button.upper())
        if command:
            self.send_command(command)
        else:
            raise ValueError(f"Unsupported button: {button}")

    def read_captured_clicks(self, button: str) -> int:
        command = {
            "LEFT": "km.catch_ml()",
            "RIGHT": "km.catch_mr()",
            "MIDDLE": "km.catch_mm()",
            "MOUSE4": "km.catch_ms1()",
            "MOUSE5": "km.catch_ms2()",
        }.get(button.upper())
        if command:
            result = self.send_command(command, expect_response=True)
            try:
                return int(result.strip())
            except Exception:
                return 0
        else:
            raise ValueError(f"Unsupported button: {button}")

    def _listen(self, debug=False):
        self._log("Started listener thread")
        last_value = None
        button_states = {i: False for i in self.button_map}
        self._last_mask = 0

        while self._is_connected and not self._stop_event.is_set():
            if self._pause_listener:
                time.sleep(0.001)
                continue
            try:
                byte = self.serial.read(1)
                if byte:
                    value = byte[0]
                    mask = 0
                    for bit, name in self.button_map.items():
                        is_pressed = bool(value & (1 << bit))
                        if is_pressed != button_states[bit]:
                            button_states[bit] = is_pressed
                        if is_pressed:
                            mask |= (1 << bit)

                    for bit, name in self.button_map.items():
                        self._button_states[name] = button_states[bit]

                    now = time.time() * 1000 
                    if self._button_callback and mask != self._last_mask:
                        for bit, name in self.button_map.items():
                            previous = bool(self._last_mask & (1 << bit))
                            current = bool(mask & (1 << bit))
                            if previous != current:
                                last_time = self._last_callback_time.get(bit, 0)
                                if now - last_time >= self._debounce_time_ms:
                                    button_enum = self._button_enum_map.get(bit)
                                    if button_enum:
                                        self._button_callback(button_enum, current)
                                        self._last_callback_time[bit] = now

                    self._last_mask = mask

                    if debug:
                        pressed = [name for bit, name in self.button_map.items() if button_states[bit]]
                        button_str = ", ".join(pressed) if pressed else "No buttons pressed"
                        self._log(f"Byte: {value} (0x{value:02X}) -> {button_str}")

                    last_value = value
            except serial.SerialException as e:
                if "ClearCommError failed" not in str(e):
                    self._log(f"Serial error during listening: {e}")
                    break
            time.sleep(0.0001)

        self._log("Listener thread exiting")