# test_is_button_pressed.py

import pytest
from makcu import create_controller, MouseButton

@pytest.fixture(scope="module")
def makcu():
    ctrl = create_controller()
    yield ctrl
    ctrl.disconnect()

def test_is_button_pressed(makcu):
    assert makcu.is_button_pressed(MouseButton.LEFT) in [True, False]