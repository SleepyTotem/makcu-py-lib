from .enums import MouseButton
from .errors import MakcuCommandError
from serial.tools import list_ports
import time

class Mouse:
    def __init__(self, transport):
        self.transport = transport

    def _send_button_command(self, button: MouseButton, state: int):
        command_map = {
            MouseButton.LEFT: "left",
            MouseButton.RIGHT: "right",
            MouseButton.MIDDLE: "middle",
            MouseButton.MOUSE4: "ms1",
            MouseButton.MOUSE5: "ms2",
        }
        if button not in command_map:
            raise MakcuCommandError(f"Unsupported button: {button}")
        self.transport.send_command(f"km.{command_map[button]}({state})")

    def press(self, button: MouseButton):
        self._send_button_command(button, 1)

    def release(self, button: MouseButton):
        self._send_button_command(button, 0)

    def move(self, x: int, y: int):
        self.transport.send_command(f"km.move({x},{y})")

    def move_smooth(self, x: int, y: int, segments: int):
        self.transport.send_command(f"km.move({x},{y},{segments})")

    def move_bezier(self, x: int, y: int, segments: int, ctrl_x: int, ctrl_y: int):
        self.transport.send_command(f"km.move({x},{y},{segments},{ctrl_x},{ctrl_y})")

    def scroll(self, delta: int):
        self.transport.send_command(f"km.wheel({delta})")

    def lock_left(self, lock: bool):
        self.transport.send_command(f"km.lock_ml({int(lock)})")
        
    def lock_middle(self, lock: bool):
        self.transport.send_command(f"km.lock_mm({int(lock)})")

    def lock_right(self, lock: bool):
        self.transport.send_command(f"km.lock_mr({int(lock)})")

    def lock_side1(self, lock: bool):
        self.transport.send_command(f"km.lock_ms1({int(lock)})")

    def lock_side2(self, lock: bool):
        self.transport.send_command(f"km.lock_ms2({int(lock)})")

    def lock_x(self, lock: bool):
        self.transport.send_command(f"km.lock_mx({int(lock)})")

    def lock_y(self, lock: bool):
        self.transport.send_command(f"km.lock_my({int(lock)})")


    def spoof_serial(self, serial: str):
        self.transport.send_command(f"km.serial('{serial}')")

    def reset_serial(self):
        self.transport.send_command("km.serial(0)")

    def get_device_info(self) -> dict:
        port_name = self.transport.port
        is_connected = self.transport.is_connected()
        info = {
            "port": port_name,
            "description": "Unknown",
            "vid": "Unknown",
            "pid": "Unknown",
            "isConnected": is_connected
        }
        for port in list_ports.comports():
            if port.device == port_name:
                info.update({
                    "description": port.description,
                    "vid": hex(port.vid) if port.vid is not None else "Unknown",
                    "pid": hex(port.pid) if port.pid is not None else "Unknown"
                })
                break
        return info

    def get_firmware_version(self) -> str:
        return self.transport.send_command("km.version()", expect_response=True)

    def _get_lock_command(self, target: str) -> str:
        command_map = {
            "X": "mx", "Y": "my",
            "LEFT": "ml", "RIGHT": "mr", "MIDDLE": "mm",
            "MOUSE4": "ms1", "MOUSE5": "ms2",
        }
        key = target.upper()
        if key not in command_map:
            raise ValueError(f"Unsupported lock target: {target}")
        return f"km.lock_{command_map[key]}()"

    def is_locked(self, button: MouseButton) -> bool:
        try:
            # Sleep for previous command to finish first, hoping to get rid of this soon.
            time.sleep(0.03)

            command = self._get_lock_command(button.name)
            result = self.transport.send_command(command, expect_response=True)
            if hasattr(self.transport, 'debug') and self.transport.debug:
                print(f"Lock status command: {command}")
                print(f"Raw result: '{result}'")
            
            result = result.strip()
            
            if result in ['1', '0']:
                return result == '1'
            
            lines = result.split('\n')
            for line in lines:
                line = line.strip()
                if line in ['1', '0']:
                    return line == '1'
            
            import re
            numbers = re.findall(r'\b[01]\b', result)
            if numbers:
                return numbers[-1] == '1'
            
            if hasattr(self.transport, 'debug') and self.transport.debug:
                print(f"Could not parse lock status from: '{result}'")
            
            return False
            
        except Exception as e:
            if hasattr(self.transport, 'debug') and self.transport.debug:
                print(f"Error checking lock status: {e}")
            return False

    def get_all_lock_states(self) -> dict:
        """Get all lock states - no timing delays needed with acknowledgment"""
        targets = ["X", "Y", "LEFT", "RIGHT", "MIDDLE", "MOUSE4", "MOUSE5"]
        state = {}
        
        for target in targets:
            try:
                # No sleep needed - each command waits for acknowledgment
                if hasattr(MouseButton, target):
                    state[target] = self.is_locked(MouseButton[target])
                else:
                    # Handle X and Y axis locks
                    if target in ["X", "Y"]:
                        # Create a mock enum-like object for axis locks
                        class AxisButton:
                            def __init__(self, name):
                                self.name = name
                        state[target] = self.is_locked(AxisButton(target))
                    else:
                        state[target] = False
            except Exception as e:
                if hasattr(self.transport, 'debug') and self.transport.debug:
                    print(f"Error getting lock state for {target}: {e}")
                state[target] = False
        
        if hasattr(self.transport, 'debug') and self.transport.debug:
            print(f"All lock states: {state}")
        
        return state