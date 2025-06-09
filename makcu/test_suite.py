import pytest, time
from makcu import MouseButton

def test_press_and_release(makcu):
    makcu.press(MouseButton.LEFT)
    makcu.release(MouseButton.LEFT)

def test_firmware_version(makcu):
    version = makcu.mouse.get_firmware_version()
    assert version and len(version.strip()) > 0

def test_middle_click(makcu):
    makcu.press(MouseButton.MIDDLE)
    makcu.release(MouseButton.MIDDLE)

def test_device_info(makcu):
    print("Fetching device info...")
    info = makcu.mouse.get_device_info()
    print(f"Device Info: {info}")
    assert info.get("port")
    assert info.get("isConnected") is True

def test_port_connection(makcu):
    assert makcu.is_connected()

@pytest.mark.skip(reason="Capture test disabled until firmware supports tracking clicks from software input")
def test_capture_right_clicks(makcu):
    makcu.mouse.lock_right(True)
    assert makcu.mouse.is_locked(MouseButton.RIGHT)

    makcu.mouse.begin_capture("RIGHT")
    makcu.press(MouseButton.RIGHT)
    makcu.mouse.release(MouseButton.RIGHT)
    makcu.press(MouseButton.RIGHT)
    makcu.mouse.release(MouseButton.RIGHT)

    makcu.mouse.lock_right(False)
    assert not makcu.mouse.is_locked(MouseButton.RIGHT)

    count = makcu.mouse.stop_capturing_clicks("RIGHT")
    assert count >= 2, f"Expected >=2 captured clicks, got {count}"

def test_button_mask(makcu):
    print("Getting button mask...")
    mask = makcu.get_button_mask()
    print(f"Mask value: {mask}")
    assert isinstance(mask, int)

def test_get_button_states(makcu):
    states = makcu.get_button_states()
    assert isinstance(states, dict)
    for key in ['left', 'right', 'middle', 'mouse4', 'mouse5']:
        assert key in states

def test_lock_state(makcu):
    print("Locking LEFT button...")
    makcu.lock_left(True)
    print("Querying lock state while LEFT is locked...")
    state = makcu.is_locked(MouseButton.LEFT)  # Check state AFTER ensuring it's locked
    print(state)
    assert state  # Now assert the current state

def test_makcu_behavior(makcu):
    makcu.move(25, 25)
    makcu.click(MouseButton.LEFT)
    makcu.scroll(-2)

def test_reset_all(makcu):
    makcu.mouse.lock_left(False)
    makcu.mouse.lock_right(False)
    makcu.mouse.lock_middle(False)
    makcu.mouse.lock_side1(False)
    makcu.mouse.lock_side2(False)
    makcu.mouse.lock_x(False)
    makcu.mouse.lock_y(False)

    states = makcu.mouse.get_all_lock_states()
    assert all(state is False for state in states.values() if state is not None), \
        f"Expected all unlocked, got: {states}"

    makcu.enable_button_monitoring(False)