from .controller import MakcuController
from .enums import MouseButton
from .errors import MakcuError, MakcuConnectionError

def create_controller(fallback_com_port="", debug=False, send_init=True):
    makcu = MakcuController(fallback_com_port, debug=debug, send_init=send_init)
    makcu.connect()
    return makcu

__all__ = [
    "MakcuController",
    "MouseButton",
    "MakcuError",
    "MakcuConnectionError",
    "create_controller",
]