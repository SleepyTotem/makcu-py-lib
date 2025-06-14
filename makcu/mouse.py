from typing import Dict, Optional, List, Union, Any
from .enums import MouseButton
from .connection import SerialTransport
from .errors import MakcuCommandError
from serial.tools import list_ports
import time

# Create a mock enum-like object for axis locks
class AxisButton:
    def __init__(self, name: str) -> None:
        self.name = name

class Mouse:
    """Ultra-optimized mouse control for gaming performance"""
    
    # Pre-computed command strings for faster access
    _BUTTON_COMMANDS = {
        MouseButton.LEFT: "left",
        MouseButton.RIGHT: "right",
        MouseButton.MIDDLE: "middle",
        MouseButton.MOUSE4: "ms1",
        MouseButton.MOUSE5: "ms2",
    }
    
    # Pre-formatted commands cache
    _PRESS_COMMANDS = {}
    _RELEASE_COMMANDS = {}
    _LOCK_COMMANDS = {}
    _UNLOCK_COMMANDS = {}
    _LOCK_QUERY_COMMANDS = {}
    
    def __init__(self, transport: SerialTransport) -> None:
        self.transport = transport
        self._lock_states_cache: int = 0  # Bitwise cache
        self._cache_valid = False
        
        # Pre-compute all commands for zero-overhead execution
        self._init_command_cache()
    
    def _init_command_cache(self) -> None:
        """Pre-compute all commands to avoid string formatting during execution"""
        # Button press/release commands
        for button, cmd in self._BUTTON_COMMANDS.items():
            self._PRESS_COMMANDS[button] = f"km.{cmd}(1)"
            self._RELEASE_COMMANDS[button] = f"km.{cmd}(0)"
        
        # Lock commands with bitwise indexing
        # Bit 0-4: buttons, Bit 5: X axis, Bit 6: Y axis
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
        """Optimized button command sending"""
        if button not in self._BUTTON_COMMANDS:
            raise MakcuCommandError(f"Unsupported button: {button}")
        
        # Use pre-computed commands
        cmd = self._PRESS_COMMANDS[button] if state else self._RELEASE_COMMANDS[button]
        self.transport.send_command(cmd)

    def press(self, button: MouseButton) -> None:
        """Press with pre-computed command"""
        self.transport.send_command(self._PRESS_COMMANDS[button])

    def release(self, button: MouseButton) -> None:
        """Release with pre-computed command"""
        self.transport.send_command(self._RELEASE_COMMANDS[button])

    def move(self, x: int, y: int) -> None:
        """Move command"""
        self.transport.send_command(f"km.move({x},{y})")

    def click(self, button: MouseButton) -> None:
        """Optimized click with cached commands"""
        if button not in self._BUTTON_COMMANDS:
            raise MakcuCommandError(f"Unsupported button: {button}")
        
        # Use pre-computed commands for maximum speed
        press_cmd = self._PRESS_COMMANDS[button]
        release_cmd = self._RELEASE_COMMANDS[button]
        
        # Send both commands in rapid succession
        transport = self.transport  # Cache reference
        transport.send_command(press_cmd)
        transport.send_command(release_cmd)

    def move_smooth(self, x: int, y: int, segments: int) -> None:
        """Smooth movement"""
        self.transport.send_command(f"km.move({x},{y},{segments})")

    def move_bezier(self, x: int, y: int, segments: int, ctrl_x: int, ctrl_y: int) -> None:
        """Bezier movement"""
        self.transport.send_command(f"km.move({x},{y},{segments},{ctrl_x},{ctrl_y})")

    def scroll(self, delta: int) -> None:
        """Scroll command"""
        self.transport.send_command(f"km.wheel({delta})")

    # Optimized lock methods using bitwise cache
    def _set_lock(self, name: str, lock: bool) -> None:
        """Generic lock setter with cache update"""
        if lock:
            cmd, bit = self._LOCK_COMMANDS[name]
        else:
            cmd, bit = self._UNLOCK_COMMANDS[name]
        
        self.transport.send_command(cmd)
        
        # Update cache
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
        """Set custom serial"""
        self.transport.send_command(f"km.serial('{serial}')")

    def reset_serial(self) -> None:
        """Reset serial"""
        self.transport.send_command("km.serial(0)")

    def get_device_info(self) -> Dict[str, Union[str, bool]]:
        """Ultra-fast device info with minimal port scanning"""
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
                    break  # Found our port, exit immediately
        except Exception:
            pass
        
        return info

    def get_firmware_version(self) -> str:
        """Get firmware version"""
        response = self.transport.send_command("km.version()", expect_response=True, timeout=0.1)
        return response or ""

    def _invalidate_cache(self) -> None:
        """Invalidate cache"""
        self._cache_valid = False

    def get_all_lock_states(self) -> Dict[str, bool]:
        """Get all lock states with parallel queries for gaming performance"""
        # Return cache if valid
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
        
        # Query all states in rapid succession
        states = {}
        targets = ["X", "Y", "LEFT", "RIGHT", "MIDDLE", "MOUSE4", "MOUSE5"]
        
        for target in targets:
            cmd, bit = self._LOCK_QUERY_COMMANDS[target]
            try:
                result = self.transport.send_command(cmd, expect_response=True, timeout=0.05)
                if result and result.strip() in ['0', '1']:
                    is_locked = result.strip() == '1'
                    states[target] = is_locked
                    
                    # Update cache
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
        """Check lock state with cache"""
        try:
            target_name = button.name if hasattr(button, 'name') else str(button)
            
            # Check cache first
            if self._cache_valid and target_name in self._LOCK_QUERY_COMMANDS:
                _, bit = self._LOCK_QUERY_COMMANDS[target_name]
                return bool(self._lock_states_cache & (1 << bit))
            
            # Query device
            cmd, bit = self._LOCK_QUERY_COMMANDS[target_name]
            result = self.transport.send_command(cmd, expect_response=True, timeout=0.05)
            
            if not result:
                return False
            
            result = result.strip()
            is_locked = result == '1'
            
            # Update cache
            if is_locked:
                self._lock_states_cache |= (1 << bit)
            else:
                self._lock_states_cache &= ~(1 << bit)
            
            return is_locked
            
        except Exception:
            return False