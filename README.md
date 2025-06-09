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

---

## 🧠 Quickstart (Python)

```python
from makcu import create_controller, MouseButton

makcu = create_controller("COM1")
makcu.click(MouseButton.LEFT)
makcu.move(100, 50)
makcu.scroll(-1)
makcu.disconnect()
```

---

## 🧩 API Reference

### 🔧 Initialization

```python
makcu = create_controller(fallback_com_port="COM1", debug=True, send_init=True)
```

---

### 🎮 Mouse Control

#### Button Actions

```python
makcu.click(MouseButton.LEFT)
makcu.press(MouseButton.RIGHT)
makcu.release(MouseButton.RIGHT)
```

#### Movement

```python
makcu.move(30, 20)
makcu.move_smooth(100, 40, segments=10)
makcu.move_bezier(50, 50, 15, ctrl_x=25, ctrl_y=25)
```

#### Scroll Wheel

```python
makcu.scroll(-3)
makcu.scroll(3)
```

---

### 🔒 Locking

```python
makcu.lock_left(True)
makcu.lock_right(True)
makcu.lock_middle(False)
makcu.lock_side1(True)
makcu.lock_side2(False)
makcu.lock_mouse_x(True)
makcu.lock_mouse_y(False)
```

#### Lock State Query

```python
makcu.is_locked(MouseButton.LEFT)
makcu.get_all_lock_states()
```

---

### 👤 Human-like Click Simulation

```python
makcu.click_human_like(
    button=MouseButton.LEFT,
    count=5,
    profile="normal",  # or "fast", "slow"
    jitter=3
)
```

---

### 🔍 Device Info & Firmware

```python
info = makcu.get_device_info()
version = makcu.get_firmware_version()
```

---

### 🔐 Serial Spoofing

```python
makcu.spoof_serial("FAKE123456")
makcu.reset_serial()
```

---

## 🧪 Button Monitoring

### Enable Monitoring

```python
makcu.enable_button_monitoring(True)
```

### Set Event Callback

```python
def on_button_event(button, pressed):
    print(f"{button.name} is {'pressed' if pressed else 'released'}")

makcu.set_button_callback(on_button_event)
```

---

## ❌ Click Capturing (Pending Firmware Fix)

```python
makcu.mouse.lock_right(True)
makcu.mouse.begin_capture("RIGHT")

# Simulated user input...

makcu.mouse.lock_right(False)
count = makcu.mouse.stop_capturing_clicks("RIGHT")
print(f"Captured clicks: {count}")
```

> ⚠️ Not fully supported yet — firmware must be updated to complete this feature.

---

## 🔢 Bitmask & Button States

```python
mask = makcu.get_button_mask()
states = makcu.get_button_states()

if makcu.is_pressed(MouseButton.RIGHT):
    print("Right button is currently pressed")
```

---

## ⚙️ Low-Level Access

```python
response = makcu.transport.send_command("km.version()", expect_response=True)
```

---

## 🧪 Test Suite

Run full test suite and generate an HTML report:

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

- Communicates via CH343 USB serial
- Automatically finds correct port or uses fallback
- Switches baud to 4M after initial connect
- Enables `km.buttons(1)` on init if requested
- Supports full button state tracking with events

---

## 📜 License

GPL License © SleepyTotem

---

## 🙋 Support

Open an issue on GitHub if you encounter bugs or need help.

## 🌐 Links

- [GitHub Repo](https://github.com/SleepyTotem/makcu-py-lib)
- [PyPI Package](https://pypi.org/project/makcu/)