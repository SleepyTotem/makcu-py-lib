# 🖱️ Makcu Python Library

Makcu Py Lib is a Python library for controlling Makcu devices — enabling software-driven mouse input, movement simulation, locking, monitoring, and more.

---

## 📦 Installation

### ✅ Recommended: PyPI

```bash
pip install makcu
```

### 🧪 Alternative: Install from Source

```bash
git clone https://github.com/SleepyTotem/makcu-py-lib
cd makcu-py-lib
pip install .
```

---

## 🚀 Command-Line Usage

After installation, use:

```bash
python -m makcu [command]
```

### Available Commands

| Command | Description |
|---------|-------------|
| `--debug` | Opens interactive console to send raw `km.*` commands |
| `--testPort COM3` | Tests a specific COM port for connectivity |
| `--runtest` | Runs all automated tests and opens a test report |

### Examples

```bash
python -m makcu --debug
python -m makcu --testPort COM3
python -m makcu --runtest
```

---

## 🧠 Quickstart (Python)

```python
from makcu import create_controller, MouseButton

makcu = create_controller("COM1") # Fallback port
makcu.click(MouseButton.LEFT)
makcu.move(100, 50)
makcu.scroll(-1)
makcu.disconnect()
```

---

## 🧩 API Reference

### 🔧 Initialization

```python
makcu = create_controller(debug=True, send_init=True)
```

#### Set fallback port manually

```python
makcu = create_controller("COM4")  # Optional fallback com port
```

---

### 🎮 Mouse Control

#### Clicks

```python
makcu.click(MouseButton.LEFT)
makcu.press(MouseButton.RIGHT)
makcu.release(MouseButton.RIGHT)
```

#### Movement

```python
makcu.move(dx=30, dy=20)
makcu.move_smooth(100, 40, segments=10)
makcu.move_bezier(50, 50, 15, ctrl_x=25, ctrl_y=25)
```

#### Scrolling

```python
makcu.scroll(-3)  # Scroll down
makcu.scroll(3)   # Scroll up
```

---

### 🔒 Locking and Unlocking

```python
makcu.lock_left(True)
makcu.lock_right(True)
makcu.lock_middle(False)
makcu.lock_side1(True)
makcu.lock_side2(False)
makcu.lock_mouse_x(True)
makcu.lock_mouse_y(False)
```

#### Lock Status

```python
makcu.is_button_locked(MouseButton.LEFT)
makcu.get_all_lock_states()
```

---

### 👤 Human-like Click Simulation

```python
makcu.click_human_like(
    button=MouseButton.LEFT,
    count=5,
    profile="normal",  # "fast", "slow" also available
    jitter=3
)
```

---

### 🔍 Device Info & Firmware

```python
info = makcu.get_device_info()
print(info)

version = makcu.get_firmware_version()
print(version)
```

---

### 🔐 Serial Spoofing

```python
makcu.spoof_serial("FAKE123456")
makcu.reset_serial()
```

---

## 🧪 Button Monitoring & Capture

### Enable Real-time Monitoring

```python
makcu.enable_button_monitoring(True)
```

### Set Callback Function

```python
def on_button_event(button, pressed):
    print(f"{button.name} is {'pressed' if pressed else 'released'}")

makcu.set_button_callback(on_button_event)
```

---

## ❌ Click Capturing (Pending Firmware Update)

Click capturing will allow you to detect and count click events in software.

```python
makcu.mouse.lock_right(True)
makcu.capture(MouseButton.RIGHT)

# User clicks however many times

makcu.mouse.lock_right(False)
count = makcu.get_captured_clicks(MouseButton.RIGHT)
print(f"Captured clicks: {count}")
```

> ⚠️ This feature is currently broken in firmware. Do not rely on it yet.

---

## 🔢 Bitmask & Button States

### Get Bitmask of Active Buttons

```python
mask = makcu.get_button_mask()
print(f"Button mask: {mask}")
```

### Get Raw Button State Map

```python
states = makcu.get_button_states()
print(states)  # {'left': False, 'right': True, ...}
```

### Check if a Specific Button Is Pressed

```python
if makcu.is_button_pressed(MouseButton.RIGHT):
    print("Right button is pressed")
```

---

## ⚙️ Low-Level Command Access

### Send raw serial commands

```python
from makcu import create_controller
makcu = create_controller()
response = makcu.transport.send_command("km.version()", expect_response=True)
print(response)
```

---

## 🧪 Test Suite

Run all tests and generate HTML report:

```bash
python -m makcu --runtest
```

---

## 📚 Enumerations

```python
from makcu import MouseButton

MouseButton.LEFT
MouseButton.RIGHT
MouseButton.MIDDLE
MouseButton.MOUSE4
MouseButton.MOUSE5
```

---

## 🧯 Exception Handling

```python
from makcu import MakcuError, MakcuConnectionError

try:
    makcu = create_controller()
except MakcuConnectionError as e:
    print("Connection failed:", e)
```

---

## 🛠️ Developer Notes

- Uses CH343 USB Serial
- Auto-connects to correct port or fallback
- Supports baud rate switching to 4M
- Automatically enables `km.buttons(1)` monitoring if `send_init=True`
- Supports raw button state polling

---

## 📜 License

GPL License © SleepyTotem

---

## Support
Please open an issue on the project repository and I will get to it asap

## 🌐 Links

- 🔗 [Project Homepage](https://github.com/SleepyTotem/makcu-py-lib)
- 🔗 [PyPi Homepage](https://pypi.org/project/makcu/)