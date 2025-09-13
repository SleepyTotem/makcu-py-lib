# 🖱️ Makcu Python Library v2.2.0

[![PyPI Version](https://img.shields.io/pypi/v/makcu.svg)](https://pypi.org/project/makcu/)
[![Python Support](https://img.shields.io/pypi/pyversions/makcu.svg)](https://pypi.org/project/makcu/)
[![License](https://img.shields.io/badge/license-GPL-blue.svg)](LICENSE)

Makcu Py Lib is a high-performance Python library for controlling Makcu devices — now with **async/await support**, **zero-delay command execution**, and **automatic reconnection**!

---

## 📦 Installation

### Recommended: PyPI

```bash
pip install makcu
```

### From Source

```bash
git clone https://github.com/SleepyTotem/makcu-py-lib
cd makcu-py-lib
pip install .
```

---

## 🧠 Quick Start

### Synchronous API (Classic)

```python
from makcu import create_controller, MouseButton

# Create and connect
makcu = create_controller(debug=True, auto_reconnect=True)

# Basic operations
makcu.click(MouseButton.LEFT)
makcu.move(100, 50)
makcu.scroll(-1)

# Human-like interaction
makcu.click_human_like(MouseButton.LEFT, count=2, profile="gaming", jitter=3)

# Clean disconnect
makcu.disconnect()
```

### Asynchronous API (New!)

```python
import asyncio
from makcu import create_async_controller, MouseButton

async def main():
    # Auto-connect with context manager
    async with await create_async_controller(debug=True) as makcu:
        # Parallel operations
        await asyncio.gather(
            makcu.move(100, 0),
            makcu.click(MouseButton.LEFT),
            makcu.scroll(-1)
        )
        
        # Human-like clicking
        await makcu.click_human_like(MouseButton.RIGHT, count=3)

asyncio.run(main())
```

---

## 🎮 Core Features

### Mouse Control

```python
# Button actions
await makcu.click(MouseButton.LEFT)
await makcu.double_click(MouseButton.RIGHT)
await makcu.press(MouseButton.MIDDLE)
await makcu.release(MouseButton.MIDDLE)

# Movement
await makcu.move(100, 50)  # Relative movement
await makcu.move_smooth(200, 100, segments=20)  # Smooth interpolation
await makcu.move_bezier(150, 150, segments=30, ctrl_x=75, ctrl_y=200)  # Bezier curve

# Scrolling
await makcu.scroll(-5)  # Scroll down
await makcu.scroll(3)   # Scroll up

# Dragging
await makcu.drag(0, 0, 300, 200, button=MouseButton.LEFT, duration=1.5)
```

### Button & Axis Locking

```python
# New unified locking API
await makcu.lock(MouseButton.LEFT)    # Lock left button
await makcu.unlock(MouseButton.RIGHT)  # Unlock right button
await makcu.lock("X")                  # Lock X-axis movement
await makcu.unlock("Y")                # Unlock Y-axis movement

# Query lock states (no delays!)
is_locked = await makcu.is_locked(MouseButton.LEFT)
all_states = await makcu.get_all_lock_states()
# Returns: {"LEFT": True, "RIGHT": False, "X": True, ...}
```

### Human-like Interactions

```python
# Realistic clicking with timing variations
await makcu.click_human_like(
    button=MouseButton.LEFT,
    count=5,
    profile="gaming",  # "fast", "normal", "slow", "variable", "gaming"
    jitter=5  # Random mouse movement between clicks
)
```

### Button Event Monitoring

```python
# Real-time button monitoring
def on_button_event(button: MouseButton, pressed: bool):
    print(f"{button.name} {'pressed' if pressed else 'released'}")

makcu.set_button_callback(on_button_event)
await makcu.enable_button_monitoring(True)

# Check current button states
states = makcu.get_button_states()
if makcu.is_pressed(MouseButton.RIGHT):
    print("Right button is pressed")
```

### Connection Management

```python
# Auto-reconnection on disconnect
makcu = await create_async_controller(auto_reconnect=True)

# Connection status callbacks
@makcu.on_connection_change
async def handle_connection(connected: bool):
    if connected:
        print("Device reconnected!")
    else:
        print("Device disconnected!")

# Manual reconnection
if not makcu.is_connected():
    await makcu.connect()
```

---

## 🔧 Advanced Features

### Batch Operations

```python
# Execute multiple commands efficiently
async def combo_action():
    await makcu.batch_execute([
        lambda: makcu.move(50, 0),
        lambda: makcu.click(MouseButton.LEFT),
        lambda: makcu.move(-50, 0),
        lambda: makcu.click(MouseButton.RIGHT)
    ])
```

### Device Information

```python
# Get device details
info = await makcu.get_device_info()
# {'port': 'COM3', 'vid': '0x1a86', 'pid': '0x55d3', ...}

# Firmware version
version = await makcu.get_firmware_version()
```

### Serial Spoofing

```python
# Spoof device serial
await makcu.spoof_serial("CUSTOM123456")

# Reset to default
await makcu.reset_serial()
```

### Low-Level Access

```python
# Send raw commands with tracked responses
response = await makcu.transport.async_send_command(
    "km.version()", 
    expect_response=True,
    timeout=0.1  # Optimized for gaming
)
```

---

## 🧪 Command-Line Tools

```bash
# Interactive debug console
python -m makcu --debug

# Test specific port
python -m makcu --testPort COM3

# Run automated tests
python -m makcu --runtest
```

### Tool Descriptions

- `--debug`: Launches an interactive console where you can type raw device commands and see live responses.
- `--testPort COMx`: Attempts to connect to the given COM port and reports success or failure.
- `--runtest`: Runs `test_suite.py` using `pytest` and opens a detailed HTML test report.

---

### Test Suite

- File: `test_suite.py`
- Run with: `python -m makcu --runtest`
- Output: `latest_pytest.html`

Includes tests for:
- Port connection
- Firmware version check
- Mouse movement and button control
- Button masking and locking

---

## Test Timings (v1.3 vs v1.4 vs v2.0)

| Test Name                | v1.3   | v1.4  | v2.0  | Improvement (v1.3 → v2.0) |
|--------------------------|--------|-------|-------|----------------------------|
| connect_to_port          | ~100ms | ~55ms | **46ms** | ~2.2x faster              |
| press_and_release        | ~18ms  | ~9ms  | **1ms**  | ~18x faster               |
| firmware_version         | ~20ms  | ~9ms  | **1ms**  | ~20x faster               |
| middle_click             | ~18ms  | ~9ms  | **1ms**  | ~18x faster               |
| device_info              | ~25ms  | ~13ms | **6ms**  | ~4.1x faster              |
| port_connection          | ~20ms  | ~9ms  | **1ms**  | ~20x faster               |
| button_mask              | ~17ms  | ~8ms  | **1ms**  | ~17x faster               |
| get_button_states        | ~18ms  | ~9ms  | **1ms**  | ~18x faster               |
| lock_state               | ~33ms  | ~10ms | **1ms**  | ~33x faster               |
| makcu_behavior           | ~20ms  | ~10ms | **1ms**  | ~20x faster               |
| batch_commands           | ~350ms | ~90ms | **3ms**  | ~117x faster              |
| rapid_moves              | ~17ms  | ~8ms  | **2ms**  | ~8.5x faster              |
| button_performance       | ~18ms  | ~9ms  | **2ms**  | ~9x faster                |
| mixed_operations         | ~22ms  | ~10ms | **2ms**  | ~11x faster               |

Based on the measured test suite, v2.0 is on average **~17× faster** than v1.3 across all core operations.


### Gaming Performance Targets (v2.0)

- **144Hz Gaming**: 7ms frame time — ✅ Easily met (avg 1–3ms per operation)
- **240Hz Gaming**: 4.2ms frame time — ✅ Consistently met (most ops ≤ 2ms)
- **360Hz Gaming**: 2.8ms frame time — ⚡ Achievable for atomic/single ops

---

## 🏎️ Performance Optimization Details

### Version History & Performance

- **v1.3 and earlier**: Original implementation with sleep delays
- **v1.4**: Initial optimizations, removed some sleep delays
- **v2.0**: Complete rewrite with zero-delay architecture

### Key Optimizations in v2.0

1. **Pre-computed Commands**: All commands are pre-formatted at initialization
2. **Bitwise Operations**: Button states use single integer with bit manipulation
3. **Zero-Copy Buffers**: Pre-allocated buffers for parsing
4. **Reduced Timeouts**: Gaming-optimized timeouts (100ms default)
5. **Cache Everything**: Connection states, lock states, and device info cached
6. **Minimal Allocations**: Reuse objects and avoid string formatting
7. **Fast Serial Settings**: 1ms read timeout, 10ms write timeout
8. **Optimized Listener**: Batch processing with minimal overhead

### Tips for Maximum Performance

```python
# Disable debug mode in production
makcu = create_controller(debug=False)

# Use cached connection checks
if makcu.is_connected():  # Cached, no serial check
    makcu.click(MouseButton.LEFT)

# Batch similar operations
with makcu:  # Context manager ensures connection
    for _ in range(10):
        makcu.move(10, 0)  # No connection check per call
```

---

## 🔍 Debugging

Enable debug mode for detailed logging:

```python
makcu = await create_async_controller(debug=True)

# View command flow (optimized timestamps)
# [123.456] [INFO] Sent command #42: km.move(100,50)
# [123.458] [DEBUG] Command #42 completed in 0.002s
```

---

## 🏗️ Migration from v1.x

Most code works without changes! Key differences:

```python
# v1.x (still works)
makcu = create_controller()
makcu.move(100, 100)

# v2.0 (async)
makcu = await create_async_controller()
await makcu.move(100, 100)

# v2.0 context manager (auto cleanup)
async with await create_async_controller() as makcu:
    await makcu.click(MouseButton.LEFT)
```

---

## 📚 API Reference

### Enumerations

```python
from makcu import MouseButton

MouseButton.LEFT    # Left mouse button
MouseButton.RIGHT   # Right mouse button  
MouseButton.MIDDLE  # Middle mouse button
MouseButton.MOUSE4  # Side button 1
MouseButton.MOUSE5  # Side button 2
```

### Exception Handling

```python
from makcu import MakcuError, MakcuConnectionError, MakcuTimeoutError

try:
    makcu = await create_async_controller()
except MakcuConnectionError as e:
    print(f"Connection failed: {e}")
except MakcuTimeoutError as e:
    print(f"Command timed out: {e}")
```

---

## 🛠️ Technical Details

- **Protocol**: CH343 USB serial at 4Mbps
- **Command Format**: ASCII with optional ID tracking (`command#ID`)
- **Response Format**: `>>> #ID:response` for tracked commands
- **Threading**: High-priority listener thread with async bridge
- **Auto-Discovery**: VID:PID=1A86:55D3 detection
- **Buffer Size**: 4KB read buffer, 256B line buffer
- **Cleanup Interval**: 50ms for timed-out commands

---

## 📜 License

GPL License © SleepyTotem

---

## 🙋 Support

- **Issues**: [GitHub Issues](https://github.com/SleepyTotem/makcu-py-lib/issues)

---

## 🌐 Links

- [GitHub Repository](https://github.com/SleepyTotem/makcu-py-lib)
- [PyPI Package](https://pypi.org/project/makcu/)
- [Documentation](https://makcu-py-lib.readthedocs.io/)
- [Changelog](https://makcu-py-lib.readthedocs.io/en/latest/changelog.html)