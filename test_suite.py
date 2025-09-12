import pytest
import time
from makcu import MouseButton


TEST_BUTTONS = (MouseButton.LEFT, MouseButton.RIGHT, MouseButton.MIDDLE)
BUTTON_STATE_KEYS = ('left', 'right', 'middle', 'mouse4', 'mouse5')
MOVE_COORDS = ((10, 0), (0, 10), (-10, 0), (0, -10))

def test_connect_to_port(makcu):
    print("Connecting to port...")
    makcu.connect()
    assert makcu.is_connected(), "Failed to connect to the makcu"

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

def test_button_mask(makcu):
    print("Getting button mask...")
    mask = makcu.get_button_mask()
    print(f"Mask value: {mask}")
    assert isinstance(mask, int)

def test_get_button_states(makcu):
    states = makcu.get_button_states()
    assert isinstance(states, dict)
    for key in BUTTON_STATE_KEYS:
        assert key in states

def test_lock_state(makcu):
    print("Locking LEFT button...")
    makcu.lock_left(True)
    print("Querying lock state while LEFT is locked...")
    state = makcu.is_locked(MouseButton.LEFT)
    print(state)
    assert state

def test_makcu_behavior(makcu):
    makcu.move(25, 25)
    makcu.click(MouseButton.LEFT)
    makcu.scroll(-2)

def test_batch_commands(makcu):
    print("Testing batch command execution (10 commands)...")
    
    start_time = time.perf_counter()
    

    makcu.move(10, 0)
    makcu.click(MouseButton.LEFT)
    makcu.move(0, 10)
    makcu.press(MouseButton.RIGHT)
    makcu.release(MouseButton.RIGHT)
    makcu.scroll(-1)
    makcu.move(-10, 0)
    makcu.click(MouseButton.MIDDLE)
    makcu.move(0, -10)
    makcu.scroll(1)
    
    end_time = time.perf_counter()
    elapsed_ms = (end_time - start_time) * 1000
    
    print(f"Batch execution time: {elapsed_ms:.2f}ms")
    print(f"Average per command: {elapsed_ms/10:.2f}ms")
    

    assert elapsed_ms < 50, f"Batch commands took {elapsed_ms:.2f}ms, expected < 50ms"
    

    start_time = time.perf_counter()
    for _ in range(10):
        makcu.move(5, 5)
    end_time = time.perf_counter()
    
    move_only_ms = (end_time - start_time) * 1000
    print(f"10 move commands: {move_only_ms:.2f}ms ({move_only_ms/10:.2f}ms per move)")

def test_rapid_moves(makcu):
    start = time.perf_counter_ns()
    

    makcu.move(5, 5)
    makcu.move(5, 5)
    makcu.move(5, 5)
    makcu.move(5, 5)
    makcu.move(5, 5)
    makcu.move(5, 5)
    makcu.move(5, 5)
    makcu.move(5, 5)
    makcu.move(5, 5)
    makcu.move(5, 5)
    
    elapsed_ms = (time.perf_counter_ns() - start) / 1_000_000
    print(f"10 rapid moves: {elapsed_ms:.2f}ms")
    assert elapsed_ms < 30

def test_button_performance(makcu):
    start = time.perf_counter_ns()
    

    for button in TEST_BUTTONS:
        makcu.press(button)
        makcu.release(button)
    
    elapsed_ms = (time.perf_counter_ns() - start) / 1_000_000
    print(f"Button operations: {elapsed_ms:.2f}ms")
    assert elapsed_ms < 20

def test_mixed_operations(makcu):
    start = time.perf_counter_ns()
    

    makcu.move(20, 20)
    makcu.press(MouseButton.LEFT)
    makcu.move(-20, -20)
    makcu.release(MouseButton.LEFT)
    makcu.scroll(1)
    
    elapsed_ms = (time.perf_counter_ns() - start) / 1_000_000
    print(f"Mixed operations: {elapsed_ms:.2f}ms")
    assert elapsed_ms < 15


@pytest.mark.skip(reason="Capture test disabled until firmware supports tracking clicks from software input")
def test_capture_right_clicks(makcu):
    pass