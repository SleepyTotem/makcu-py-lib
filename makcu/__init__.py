from .controller import MakcuController
from .enums import MouseButton
from .errors import MakcuError, MakcuConnectionError

def create_controller(debug=False, send_init=True):
    makcu = MakcuController(debug=debug, send_init=send_init)
    makcu.connect()
    return makcu

__all__ = [
    "MakcuController",
    "MouseButton",
    "MakcuError",
    "MakcuConnectionError",
    "create_controller",
]