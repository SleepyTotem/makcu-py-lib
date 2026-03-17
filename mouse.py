from typing import Dict, Union
from .enums import MouseButton
from .connection import SerialTransport
from .errors import MakcuCommandError
from serial.tools import list_ports
import ctypes
import time

class AxisButton:
    def __init__(self, name: str) -> None:
        self.name = name

class Mouse:
    _BUTTON_COMMANDS = {
        MouseButton.LEFT: "left",
        MouseButton.RIGHT: "right",
        MouseButton.MIDDLE: "middle",
        MouseButton.MOUSE4: "side1",
        MouseButton.MOUSE5: "side2",
    }

    _PRESS_COMMANDS = {}
    _RELEASE_COMMANDS = {}
    _LOCK_COMMANDS = {}
    _UNLOCK_COMMANDS = {}
    _LOCK_QUERY_COMMANDS = {}
    
    def __init__(self, transport: SerialTransport) -> None:
        self.transport = transport
        self._lock_states_cache: int = 0
        self._cache_valid = False
        self._init_command_cache()
    
    def _init_command_cache(self) -> None:
        for button, cmd in self._BUTTON_COMMANDS.items():
            self._PRESS_COMMANDS[button] = f"km.{cmd}(1)"
            self._RELEASE_COMMANDS[button] = f"km.{cmd}(0)"
    
        lock_targets = [
            ("LEFT", "ml", 0),
            ("RIGHT", "mr", 1),
            ("MIDDLE", "mm", 2),
            ("MOUSE4", "ms1", 3),
            ("MOUSE5", "ms2", 4),
            ("X", "mx", 5),
            ("Y", "my", 6),
        ]

        for name, cmd, bit in lock_targets:
            self._LOCK_COMMANDS[name] = (f"km.lock_{cmd}(1)", bit)
            self._UNLOCK_COMMANDS[name] = (f"km.lock_{cmd}(0)", bit)
            self._LOCK_QUERY_COMMANDS[name] = (f"km.lock_{cmd}()", bit)

    def _send_button_command(self, button: MouseButton, state: int) -> None:
        if button not in self._BUTTON_COMMANDS:
            raise MakcuCommandError(f"Unsupported button: {button}")

        cmd = self._PRESS_COMMANDS[button] if state else self._RELEASE_COMMANDS[button]
        self.transport.send_command(cmd)

    def press(self, button: MouseButton) -> None:
        self.transport.send_command(self._PRESS_COMMANDS[button])

    def release(self, button: MouseButton) -> None:
        self.transport.send_command(self._RELEASE_COMMANDS[button])

    def move(self, x: int, y: int) -> None:
        self.transport.send_command(f"km.move({x},{y})")

    def move_abs(self,
        target: tuple[int, int],
        speed: int = 1,
        wait_ms: int = 2) -> None:

        def get_mouse_speed_multiplier() -> float:
            """Return multiplier to convert pixels to mickeys based on Windows pointer speed."""
            SPI_GETMOUSESPEED = 0x0070
            speed = ctypes.c_uint()
            ctypes.windll.user32.SystemParametersInfoW(
                SPI_GETMOUSESPEED, 0, ctypes.byref(speed), 0
            )
            return speed.value / 10.0
        
        def get_cursor_pos():
            class POINT(ctypes.Structure):
                _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
            pt = POINT()
            ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
            return pt.x, pt.y
        
        multiplier = get_mouse_speed_multiplier()
        end_x, end_y = target
        
        # clamp speed to be between 1-14. >15 creates an infinite overflick loop issue.
        speed = max(1, min(speed, 14))
        
        while True:
            cx, cy = get_cursor_pos()
            dx, dy = end_x - cx, end_y - cy

            if abs(dx) <= 1 and abs(dy) <= 1:
                break
            
            move_x = max(-speed, min(speed, int(dx / multiplier)))
            move_y = max(-speed, min(speed, int(dy / multiplier)))

            self.transport.send_command(f"km.move({move_x},{move_y})")
            time.sleep(wait_ms / 1000)

    def click(self, button: MouseButton) -> None:
        if button not in self._BUTTON_COMMANDS:
            raise MakcuCommandError(f"Unsupported button: {button}")

        press_cmd = self._PRESS_COMMANDS[button]
        release_cmd = self._RELEASE_COMMANDS[button]
        
        transport = self.transport
        transport.send_command(press_cmd)
        transport.send_command(release_cmd)

    def move_smooth(self, x: int, y: int, segments: int) -> None:
        self.transport.send_command(f"km.move({x},{y},{segments})")

    def move_bezier(self, x: int, y: int, segments: int, ctrl_x: int, ctrl_y: int) -> None:
        self.transport.send_command(f"km.move({x},{y},{segments},{ctrl_x},{ctrl_y})")

    def scroll(self, delta: int) -> None:
        self.transport.send_command(f"km.wheel({delta})")


    def _set_lock(self, name: str, lock: bool) -> None:
        if lock:
            cmd, bit = self._LOCK_COMMANDS[name]
        else:
            cmd, bit = self._UNLOCK_COMMANDS[name]
        
        self.transport.send_command(cmd)
        
        if lock:
            self._lock_states_cache |= (1 << bit)
        else:
            self._lock_states_cache &= ~(1 << bit)
        self._cache_valid = True

    def lock_left(self, lock: bool) -> None:
        self._set_lock("LEFT", lock)
        
    def lock_middle(self, lock: bool) -> None:
        self._set_lock("MIDDLE", lock)

    def lock_right(self, lock: bool) -> None:
        self._set_lock("RIGHT", lock)

    def lock_side1(self, lock: bool) -> None:
        self._set_lock("MOUSE4", lock)

    def lock_side2(self, lock: bool) -> None:
        self._set_lock("MOUSE5", lock)

    def lock_x(self, lock: bool) -> None:
        self._set_lock("X", lock)

    def lock_y(self, lock: bool) -> None:
        self._set_lock("Y", lock)

    def spoof_serial(self, serial: str) -> None:
        self.transport.send_command(f"km.serial('{serial}')")

    def reset_serial(self) -> None:
        self.transport.send_command("km.serial(0)")

    def get_device_info(self) -> Dict[str, Union[str, bool]]:
        port_name = self.transport.port
        is_connected = self.transport.is_connected()
        
        if not is_connected or not port_name:
            return {
                "port": port_name or "Unknown",
                "description": "Disconnected",
                "vid": "Unknown", 
                "pid": "Unknown",
                "isConnected": False
            }
        
        info = {
            "port": port_name,
            "description": "Connected Device",
            "vid": "Unknown", 
            "pid": "Unknown",
            "isConnected": True
        }
        
        try:
            for port in list_ports.comports():
                if port.device == port_name:
                    info["description"] = port.description or "Connected Device"
                    if port.vid is not None:
                        info["vid"] = f"0x{port.vid:04x}"
                    if port.pid is not None:
                        info["pid"] = f"0x{port.pid:04x}"
                    break
        except Exception:
            pass
        
        return info

    def get_firmware_version(self) -> str:
        response = self.transport.send_command("km.version()", expect_response=True, timeout=0.1)
        return response or ""

    def _invalidate_cache(self) -> None:
        self._cache_valid = False

    def get_all_lock_states(self) -> Dict[str, bool]:

        if self._cache_valid:
            return {
                "X": bool(self._lock_states_cache & (1 << 5)),
                "Y": bool(self._lock_states_cache & (1 << 6)),
                "LEFT": bool(self._lock_states_cache & (1 << 0)),
                "RIGHT": bool(self._lock_states_cache & (1 << 1)),
                "MIDDLE": bool(self._lock_states_cache & (1 << 2)),
                "MOUSE4": bool(self._lock_states_cache & (1 << 3)),
                "MOUSE5": bool(self._lock_states_cache & (1 << 4)),
            }
        
        states = {}
        targets = ["X", "Y", "LEFT", "RIGHT", "MIDDLE", "MOUSE4", "MOUSE5"]
        
        for target in targets:
            cmd, bit = self._LOCK_QUERY_COMMANDS[target]
            try:
                result = self.transport.send_command(cmd, expect_response=True, timeout=0.05)
                if result and result.strip() in ['0', '1']:
                    is_locked = result.strip() == '1'
                    states[target] = is_locked
                    
                    if is_locked:
                        self._lock_states_cache |= (1 << bit)
                    else:
                        self._lock_states_cache &= ~(1 << bit)
                else:
                    states[target] = False
            except Exception:
                states[target] = False
        
        self._cache_valid = True
        return states

    def is_locked(self, button: Union[MouseButton, AxisButton]) -> bool:
        try:
            target_name = button.name if hasattr(button, 'name') else str(button)

            if self._cache_valid and target_name in self._LOCK_QUERY_COMMANDS:
                _, bit = self._LOCK_QUERY_COMMANDS[target_name]
                return bool(self._lock_states_cache & (1 << bit))

            cmd, bit = self._LOCK_QUERY_COMMANDS[target_name]
            result = self.transport.send_command(cmd, expect_response=True, timeout=0.05)
            
            if not result:
                return False
            
            result = result.strip()
            is_locked = result == '1'
            
            if is_locked:
                self._lock_states_cache |= (1 << bit)
            else:
                self._lock_states_cache &= ~(1 << bit)
            
            return is_locked
            
        except Exception:
            return False
