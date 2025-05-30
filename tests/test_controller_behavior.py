# test_makcu_behavior.py
from makcu import MouseButton

def test_makcu_behavior(makcu):
    makcu.move(25, 25)
    makcu.click(MouseButton.LEFT)
    makcu.scroll(-2)