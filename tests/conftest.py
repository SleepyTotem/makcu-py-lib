import pytest
import time
from makcu import create_controller

@pytest.fixture(scope="session")
def makcu():
    c = create_controller()
    yield c
    c.disconnect()
    time.sleep(0.2)

@pytest.fixture(autouse=True)
def ensure_clean_exit(makcu):
    yield
    makcu.mouse.lock_left(False)
    makcu.mouse.lock_right(False)
    makcu.mouse.lock_middle(False)
    makcu.mouse.lock_side1(False)
    makcu.mouse.lock_side2(False)
    makcu.mouse.lock_x(False)
    makcu.mouse.lock_y(False)
    makcu.enable_button_monitoring(False)