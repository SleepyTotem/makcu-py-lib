# test_press_and_release.py

import pytest
from makcu import create_controller, MouseButton

@pytest.fixture(scope="module")
def makcu():
    ctrl = create_controller()
    yield ctrl
    ctrl.disconnect()

def test_press_and_release(makcu):
    makcu.press(MouseButton.LEFT)
    makcu.release(MouseButton.LEFT)