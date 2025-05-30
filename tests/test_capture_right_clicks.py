# test_capture_right_clicks.py
import pytest
from makcu import MouseButton

@pytest.mark.skip(reason="Capture test disabled until firmware supports tracking clicks from software input")
def test_capture_right_clicks(makcu):
    makcu.mouse.lock_right(True)
    assert makcu.mouse.is_button_locked(MouseButton.RIGHT)

    makcu.mouse.begin_capture("RIGHT")

    makcu.mouse.press(MouseButton.RIGHT)
    makcu.mouse.release(MouseButton.RIGHT)
    makcu.mouse.press(MouseButton.RIGHT)
    makcu.mouse.release(MouseButton.RIGHT)

    makcu.mouse.lock_right(False)
    assert not makcu.mouse.is_button_locked(MouseButton.RIGHT)

    count = makcu.mouse.stop_capturing_clicks("RIGHT")
    assert count >= 2, f"Expected >=2 captured clicks, got {count}"