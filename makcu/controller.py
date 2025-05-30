import random
import time
from .mouse import Mouse
from .connection import SerialTransport
from .errors import MakcuConnectionError
from .enums import MouseButton

class MakcuController:
    def __init__(self, port=None, debug=False, send_init=True):
        self.transport = SerialTransport(port=port, debug=debug, send_init=send_init)
        self.mouse = Mouse(self.transport)

    def connect(self):
        self.transport.connect()

    def disconnect(self):
        self.transport.disconnect()

    def is_connected(self):
        return self.transport.is_connected()

    def _check_connection(self):
        if not self.transport.serial or not self.transport.serial.is_open:
            raise MakcuConnectionError("Not connected")

    def click(self, button: MouseButton):
        self._check_connection()
        self.mouse.press(button)
        self.mouse.release(button)

    def move(self, dx: int, dy: int):
        self._check_connection()
        self.mouse.move(dx, dy)

    def scroll(self, delta: int):
        self._check_connection()
        self.mouse.scroll(delta)

    def move_smooth(self, dx: int, dy: int, segments: int):
        self._check_connection()
        self.mouse.move_smooth(dx, dy, segments)

    def move_bezier(self, dx: int, dy: int, segments: int, ctrl_x: int, ctrl_y: int):
        self._check_connection()
        self.mouse.move_bezier(dx, dy, segments, ctrl_x, ctrl_y)

    def lock_mouse_x(self, lock: bool):
        self._check_connection()
        self.mouse.lock_x(lock)

    def lock_mouse_y(self, lock: bool):
        self._check_connection()
        self.mouse.lock_y(lock)

    def lock_left(self, lock: bool):
        self._check_connection()
        self.mouse.lock_left(lock)

    def lock_middle(self, lock: bool):
        self._check_connection()
        self.mouse.lock_middle(lock)

    def lock_right(self, lock: bool):
        self._check_connection()
        self.mouse.lock_right(lock)

    def lock_side1(self, lock: bool):
        self._check_connection()
        self.mouse.lock_side1(lock)

    def lock_side2(self, lock: bool):
        self._check_connection()
        self.mouse.lock_side2(lock)

    def spoof_serial(self, serial: str):
        self._check_connection()
        self.mouse.spoof_serial(serial)

    def reset_serial(self):
        self._check_connection()
        self.mouse.reset_serial()

    def get_device_info(self):
        self._check_connection()
        return self.mouse.get_device_info()

    def get_firmware_version(self):
        self._check_connection()
        return self.mouse.get_firmware_version()

    def get_button_mask(self) -> int:
        self._check_connection()
        return self.transport.get_button_mask()

    def is_locked(self, target: str) -> bool:
        self._check_connection()
        return self.mouse.is_locked(target)

    def is_button_locked(self, button: MouseButton) -> bool:
        self._check_connection()
        return self.mouse.is_button_locked(button)

    def capture(self, button: MouseButton):
        self._check_connection()
        self.mouse.begin_capture(button.name)

    def get_captured_clicks(self, button: MouseButton) -> int:
        self._check_connection()
        return self.mouse.stop_capturing_clicks(button.name)


    def click_human_like(self, button: MouseButton, count: int = 1,
        profile: str = "normal", jitter: int = 0):
        self._check_connection()

        timing_profiles = {
            "normal": {"min_down": 60,  "max_down": 120, "min_wait": 100, "max_wait": 180},
            "fast":   {"min_down": 30,  "max_down": 60,  "min_wait": 50,  "max_wait": 100},
            "slow":   {"min_down": 100, "max_down": 180, "min_wait": 150, "max_wait": 300},
        }

        if profile not in timing_profiles:
            raise ValueError(f"Invalid profile: {profile}. Choose from {list(timing_profiles.keys())}")

        t = timing_profiles[profile]

        for _ in range(count):
            if jitter > 0:
                dx = random.randint(-jitter, jitter)
                dy = random.randint(-jitter, jitter)
                self.mouse.move(dx, dy)

            self.mouse.press(button)
            time.sleep(random.uniform(t["min_down"], t["max_down"]) / 1000.0)
            self.mouse.release(button)
            time.sleep(random.uniform(t["min_wait"], t["max_wait"]) / 1000.0)
    
    def enable_button_monitoring(self, enable: bool = True):
        self._check_connection()
        self.transport.enable_button_monitoring(enable)

    def set_button_callback(self, callback):
        self._check_connection()
        self.transport.set_button_callback(callback)

    def get_all_lock_states(self) -> dict:
        self._check_connection()
        return self.mouse.get_all_lock_states()
    
    def set_callback_debounce_time(self, ms: int):
        self._check_connection()
        self.transport.set_debounce_time(ms)

    def start_capturing_clicks(self, button: str):
        self._check_connection()
        self.transport._capture_counts[button] = 0
        self.transport._capture_active[button] = True
        self.transport._capture_last_state[button] = None
        self.mouse.begin_capture(button)

    def stop_capturing_clicks(self, button: str) -> int:
        self._check_connection()
        self.transport._capture_active[button] = False
        return self.mouse.stop_capturing_clicks(button)

    def press(self, button: MouseButton):
        self._check_connection()
        self.mouse.press(button)

    def release(self, button: MouseButton):
        self._check_connection()
        self.mouse.release(button)

