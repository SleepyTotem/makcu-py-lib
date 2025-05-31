# test_get_raw_mask.py

import pytest
from makcu import create_controller

@pytest.fixture(scope="module")
def makcu():
    ctrl = create_controller()
    yield ctrl
    ctrl.disconnect()

def test_get_raw_mask(makcu):
    mask = makcu.get_raw_mask()
    assert isinstance(mask, int)