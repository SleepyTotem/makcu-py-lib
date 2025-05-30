from .enums import MouseButton
from .errors import MakcuCommandError
from serial.tools import list_ports

class Mouse:
    def __init__(self, transport):
        self.transport = transport

    def press(self, button: MouseButton):
        cmd = {
            MouseButton.LEFT: "km.left(1)",
            MouseButton.RIGHT: "km.right(1)",
            MouseButton.MIDDLE: "km.middle(1)"
        }.get(button)
        if cmd:
            self.transport.send_command(cmd)
        else:
            raise MakcuCommandError(f"Unsupported button for press(): {button}")

    def release(self, button: MouseButton):
        cmd = {
            MouseButton.LEFT: "km.left(0)",
            MouseButton.RIGHT: "km.right(0)",
            MouseButton.MIDDLE: "km.middle(0)"
        }.get(button)
        if cmd:
            self.transport.send_command(cmd)
        else:
            raise MakcuCommandError(f"Unsupported button for release(): {button}")

    def move(self, x: int, y: int):
        self.transport.send_command(f"km.move({x},{y})")

    def move_smooth(self, x: int, y: int, segments: int):
        self.transport.send_command(f"km.move({x},{y},{segments})")

    def move_bezier(self, x: int, y: int, segments: int, ctrl_x: int, ctrl_y: int):
        self.transport.send_command(f"km.move({x},{y},{segments},{ctrl_x},{ctrl_y})")

    def scroll(self, delta: int):
        self.transport.send_command(f"km.wheel({delta})")

    def lock_left(self, lock: bool): self.transport.send_command(f"km.lock_ml({int(lock)})")
    def lock_middle(self, lock: bool): self.transport.send_command(f"km.lock_mm({int(lock)})")
    def lock_right(self, lock: bool): self.transport.send_command(f"km.lock_mr({int(lock)})")
    def lock_side1(self, lock: bool): self.transport.send_command(f"km.lock_ms1({int(lock)})")
    def lock_side2(self, lock: bool): self.transport.send_command(f"km.lock_ms2({int(lock)})")
    def lock_x(self, lock: bool): self.transport.send_command(f"km.lock_mx({int(lock)})")
    def lock_y(self, lock: bool): self.transport.send_command(f"km.lock_my({int(lock)})")

    def spoof_serial(self, serial: str): self.transport.send_command(f"km.serial('{serial}')")
    def reset_serial(self): self.transport.send_command("km.serial(0)")

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

    def is_locked(self, target: str) -> bool:
        target = target.upper()
        commands = {
            "X": "km.lock_mx()",
            "Y": "km.lock_my()",
            "LEFT": "km.lock_ml()",
            "MIDDLE": "km.lock_mm()",
            "RIGHT": "km.lock_mr()",
            "MOUSE4": "km.lock_ms1()",
            "MOUSE5": "km.lock_ms2()",
        }
        if target not in commands:
            raise ValueError(f"Unsupported lock target: {target}")
        try:
            result = self.transport.send_command(commands[target], expect_response=True)
            return result.strip() == "1"
        except Exception:
            return False

    def is_button_locked(self, button: MouseButton) -> bool:
        name_map = {
            MouseButton.LEFT: "LEFT",
            MouseButton.RIGHT: "RIGHT",
            MouseButton.MIDDLE: "MIDDLE",
            MouseButton.MOUSE4: "MOUSE4",
            MouseButton.MOUSE5: "MOUSE5"
        }
        return self.is_locked(name_map[button])

    def begin_capture(self, button: str):
        """
        Assumes lock_<button>(1) has already been called.
        Sends catch_<button>(0) to begin capturing click cycles.
        """
        self.transport.catch_button(button)

    def stop_capturing_clicks(self, button: str) -> int:
        """
        Assumes lock_<button>(0) has already been called.
        Returns the total number of clicks since begin_capture.
        """
        return self.transport.read_captured_clicks(button)

    def get_captured_clicks_enum(self, button: MouseButton) -> int:
        mapping = {
            MouseButton.LEFT: "LEFT",
            MouseButton.RIGHT: "RIGHT",
            MouseButton.MIDDLE: "MIDDLE",
            MouseButton.MOUSE4: "MOUSE4",
            MouseButton.MOUSE5: "MOUSE5",
        }
        return self.stop_capturing_clicks(mapping[button])

    def get_all_lock_states(self) -> dict:
        return {
            target: self.is_locked(target)
            for target in ["X", "Y", "LEFT", "RIGHT", "MIDDLE", "MOUSE4", "MOUSE5"]
        }