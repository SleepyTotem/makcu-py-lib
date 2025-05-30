# test_middle_click.py
from makcu import MouseButton

def test_middle_click(makcu):
    makcu.mouse.press(MouseButton.MIDDLE)
    makcu.mouse.release(MouseButton.MIDDLE)