import pytest
import time
from makcu import MakcuController, MouseButton

@pytest.fixture(scope="session")
def makcu():
    ctrl = MakcuController(fallback_com_port="COM1", debug=False)
    return ctrl