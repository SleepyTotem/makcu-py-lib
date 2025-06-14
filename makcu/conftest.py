import pytest
import time
from makcu import MakcuController, MouseButton

@pytest.fixture(scope="session")
def makcu(request):
    ctrl = MakcuController(fallback_com_port="COM1", debug=False)

    def cleanup():
        if ctrl.is_connected():

            time.sleep(0.1)

            ctrl.lock_left(False)
            ctrl.lock_right(False)
            ctrl.lock_middle(False)
            ctrl.lock_side1(False)
            ctrl.lock_side2(False)
            ctrl.lock_x(False)
            ctrl.lock_y(False)

            ctrl.release(MouseButton.LEFT)
            ctrl.release(MouseButton.RIGHT)
            ctrl.release(MouseButton.MIDDLE)
            ctrl.release(MouseButton.MOUSE4)
            ctrl.release(MouseButton.MOUSE5)

            ctrl.enable_button_monitoring(False)

        ctrl.disconnect()

    request.addfinalizer(cleanup)

    return ctrl