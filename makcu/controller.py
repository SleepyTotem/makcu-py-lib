import asyncio
import random
import time
from typing import Optional, Dict, Callable, Union, List
from concurrent.futures import ThreadPoolExecutor
from .mouse import Mouse
from .connection import SerialTransport
from .errors import MakcuConnectionError
from .enums import MouseButton

class MakcuController:
    

    _BUTTON_LOCK_MAP = {
        MouseButton.LEFT: 'lock_left',
        MouseButton.RIGHT: 'lock_right',
        MouseButton.MIDDLE: 'lock_middle',
        MouseButton.MOUSE4: 'lock_side1',
        MouseButton.MOUSE5: 'lock_side2',
    }
    
    def __init__(self, fallback_com_port: str = "", debug: bool = False, 
                 send_init: bool = True, auto_reconnect: bool = True, 
                 override_port: bool = False) -> None:
        self.transport = SerialTransport(
            fallback_com_port, 
            debug=debug, 
            send_init=send_init,
            auto_reconnect=auto_reconnect,
            override_port=override_port
        )
        self.mouse = Mouse(self.transport)
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._connection_callbacks: List[Callable[[bool], None]] = []
        

        self._connected = False


    def connect(self) -> None:
        self.transport.connect()
        self._connected = True
        self._notify_connection_change(True)

    def disconnect(self) -> None:
        self.transport.disconnect()
        self._connected = False
        self._notify_connection_change(False)
        self._executor.shutdown(wait=False)

    def is_connected(self) -> bool:
        return self._connected and self.transport.is_connected()

    def _check_connection(self) -> None:
        if not self._connected:
            raise MakcuConnectionError("Not connected")

    def _notify_connection_change(self, connected: bool) -> None:
        for callback in self._connection_callbacks:
            try:
                callback(connected)
            except Exception:
                pass


    def click(self, button: MouseButton) -> None:
        if not self._connected:
            raise MakcuConnectionError("Not connected")
        self.mouse.press(button)
        self.mouse.release(button)

    def double_click(self, button: MouseButton) -> None:
        if not self._connected:
            raise MakcuConnectionError("Not connected")
        self.mouse.press(button)
        self.mouse.release(button)

        time.sleep(0.001)
        self.mouse.press(button)
        self.mouse.release(button)

    def move(self, dx: int, dy: int) -> None:
        if not self._connected:
            raise MakcuConnectionError("Not connected")
        self.mouse.move(dx, dy)

    def scroll(self, delta: int) -> None:
        if not self._connected:
            raise MakcuConnectionError("Not connected")
        self.mouse.scroll(delta)

    def press(self, button: MouseButton) -> None:
        if not self._connected:
            raise MakcuConnectionError("Not connected")
        self.mouse.press(button)

    def release(self, button: MouseButton) -> None:
        if not self._connected:
            raise MakcuConnectionError("Not connected")
        self.mouse.release(button)


    def move_smooth(self, dx: int, dy: int, segments: int = 10) -> None:
        if not self._connected:
            raise MakcuConnectionError("Not connected")
        self.mouse.move_smooth(dx, dy, segments)

    def move_bezier(self, dx: int, dy: int, segments: int = 20,
                    ctrl_x: Optional[int] = None, ctrl_y: Optional[int] = None) -> None:
        if not self._connected:
            raise MakcuConnectionError("Not connected")
        if ctrl_x is None:
            ctrl_x = dx // 2
        if ctrl_y is None:
            ctrl_y = dy // 2
        self.mouse.move_bezier(dx, dy, segments, ctrl_x, ctrl_y)


    def lock(self, target: Union[MouseButton, str]) -> None:
        if not self._connected:
            raise MakcuConnectionError("Not connected")
            
        if isinstance(target, MouseButton):
            if target in self._BUTTON_LOCK_MAP:
                getattr(self.mouse, self._BUTTON_LOCK_MAP[target])(True)
            else:
                raise ValueError(f"Unsupported button: {target}")
        elif target.upper() in ['X', 'Y']:
            if target.upper() == 'X':
                self.mouse.lock_x(True)
            else:
                self.mouse.lock_y(True)
        else:
            raise ValueError(f"Invalid lock target: {target}")

    def unlock(self, target: Union[MouseButton, str]) -> None:
        if not self._connected:
            raise MakcuConnectionError("Not connected")
            
        if isinstance(target, MouseButton):
            if target in self._BUTTON_LOCK_MAP:
                getattr(self.mouse, self._BUTTON_LOCK_MAP[target])(False)
            else:
                raise ValueError(f"Unsupported button: {target}")
        elif target.upper() in ['X', 'Y']:
            if target.upper() == 'X':
                self.mouse.lock_x(False)
            else:
                self.mouse.lock_y(False)
        else:
            raise ValueError(f"Invalid unlock target: {target}")


    def lock_left(self, lock: bool) -> None:
        if not self._connected:
            raise MakcuConnectionError("Not connected")
        self.mouse.lock_left(lock)

    def lock_middle(self, lock: bool) -> None:
        if not self._connected:
            raise MakcuConnectionError("Not connected")
        self.mouse.lock_middle(lock)

    def lock_right(self, lock: bool) -> None:
        if not self._connected:
            raise MakcuConnectionError("Not connected")
        self.mouse.lock_right(lock)

    def lock_side1(self, lock: bool) -> None:
        if not self._connected:
            raise MakcuConnectionError("Not connected")
        self.mouse.lock_side1(lock)

    def lock_side2(self, lock: bool) -> None:
        if not self._connected:
            raise MakcuConnectionError("Not connected")
        self.mouse.lock_side2(lock)

    def lock_x(self, lock: bool) -> None:
        if not self._connected:
            raise MakcuConnectionError("Not connected")
        self.mouse.lock_x(lock)

    def lock_y(self, lock: bool) -> None:
        if not self._connected:
            raise MakcuConnectionError("Not connected")
        self.mouse.lock_y(lock)

    def lock_mouse_x(self, lock: bool) -> None:
        self.lock_x(lock)

    def lock_mouse_y(self, lock: bool) -> None:
        self.lock_y(lock)

    def is_locked(self, button: MouseButton) -> bool:
        if not self._connected:
            raise MakcuConnectionError("Not connected")
        return self.mouse.is_locked(button)

    def get_all_lock_states(self) -> Dict[str, bool]:
        if not self._connected:
            raise MakcuConnectionError("Not connected")
        return self.mouse.get_all_lock_states()


    def spoof_serial(self, serial: str) -> None:
        if not self._connected:
            raise MakcuConnectionError("Not connected")
        self.mouse.spoof_serial(serial)

    def reset_serial(self) -> None:
        if not self._connected:
            raise MakcuConnectionError("Not connected")
        self.mouse.reset_serial()

    def get_device_info(self) -> Dict[str, str]:
        if not self._connected:
            raise MakcuConnectionError("Not connected")
        return self.mouse.get_device_info()

    def get_firmware_version(self) -> str:
        if not self._connected:
            raise MakcuConnectionError("Not connected")
        return self.mouse.get_firmware_version()


    def get_button_mask(self) -> int:
        if not self._connected:
            raise MakcuConnectionError("Not connected")
        return self.transport.get_button_mask()

    def get_button_states(self) -> Dict[str, bool]:
        if not self._connected:
            raise MakcuConnectionError("Not connected")
        return self.transport.get_button_states()

    def is_pressed(self, button: MouseButton) -> bool:
        if not self._connected:
            raise MakcuConnectionError("Not connected")
        return self.transport.get_button_states().get(button.name.lower(), False)

    def enable_button_monitoring(self, enable: bool = True) -> None:
        if not self._connected:
            raise MakcuConnectionError("Not connected")
        self.transport.enable_button_monitoring(enable)

    def set_button_callback(self, callback: Optional[Callable[[MouseButton, bool], None]]) -> None:
        if not self._connected:
            raise MakcuConnectionError("Not connected")
        self.transport.set_button_callback(callback)


    def on_connection_change(self, callback: Callable[[bool], None]) -> None:
        self._connection_callbacks.append(callback)

    def remove_connection_callback(self, callback: Callable[[bool], None]) -> None:
        if callback in self._connection_callbacks:
            self._connection_callbacks.remove(callback)


    def click_human_like(self, button: MouseButton, count: int = 1,
                        profile: str = "normal", jitter: int = 0) -> None:
        if not self._connected:
            raise MakcuConnectionError("Not connected")


        timing_profiles = {
            "normal": (60, 120, 100, 180),
            "fast": (30, 60, 50, 100),
            "slow": (100, 180, 150, 300),
            "variable": (40, 200, 80, 250),
            "gaming": (20, 40, 30, 60),
        }

        if profile not in timing_profiles:
            raise ValueError(f"Invalid profile: {profile}")

        min_down, max_down, min_wait, max_wait = timing_profiles[profile]

        for i in range(count):
            if jitter > 0:
                dx = random.randint(-jitter, jitter)
                dy = random.randint(-jitter, jitter)
                self.mouse.move(dx, dy)

            self.mouse.press(button)
            time.sleep(random.uniform(min_down, max_down) / 1000.0)
            self.mouse.release(button)
            
            if i < count - 1:
                time.sleep(random.uniform(min_wait, max_wait) / 1000.0)

    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int,
             button: MouseButton = MouseButton.LEFT, duration: float = 1.0) -> None:
        if not self._connected:
            raise MakcuConnectionError("Not connected")
        

        self.move(start_x, start_y)
        time.sleep(0.02)
        

        self.press(button)
        time.sleep(0.02)
        

        segments = max(10, int(duration * 30))
        self.move_smooth(end_x - start_x, end_y - start_y, segments)
        

        time.sleep(0.02)
        self.release(button)


    def __enter__(self):
        if not self.is_connected():
            self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()


    async def async_connect(self) -> None:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(self._executor, self.connect)

    async def async_disconnect(self) -> None:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(self._executor, self.disconnect)

    async def async_click(self, button: MouseButton) -> None:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(self._executor, self.click, button)

    async def async_move(self, dx: int, dy: int) -> None:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(self._executor, self.move, dx, dy)

    async def async_scroll(self, delta: int) -> None:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(self._executor, self.scroll, delta)


    async def __aenter__(self):
        await self.async_connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.async_disconnect()



def create_controller(fallback_com_port: str = "", debug: bool = False, 
                     send_init: bool = True, auto_reconnect: bool = True) -> MakcuController:
    makcu = MakcuController(
        fallback_com_port, 
        debug=debug, 
        send_init=send_init,
        auto_reconnect=auto_reconnect
    )
    makcu.connect()
    return makcu


async def create_async_controller(fallback_com_port: str = "", debug: bool = False,
                                 send_init: bool = True, auto_reconnect: bool = True, 
                                 override_port: bool = False) -> MakcuController:
    makcu = MakcuController(
        fallback_com_port,
        debug=debug,
        send_init=send_init,
        auto_reconnect=auto_reconnect,
        override_port=override_port
    )
    await makcu.async_connect()
    return makcu