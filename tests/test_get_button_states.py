# test_get_button_states.py

import pytest
from makcu import create_controller

@pytest.fixture(scope="module")
def makcu():
    ctrl = create_controller()
    yield ctrl
    ctrl.disconnect()

def test_get_button_states(makcu):
    states = makcu.get_button_states()
    assert isinstance(states, dict)
    for key in ['left', 'right', 'middle', 'mouse4', 'mouse5']:
        assert key in states