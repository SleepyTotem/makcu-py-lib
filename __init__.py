from .controller import (
    MakcuController,
    create_controller,
    create_async_controller,
    maybe_async
)
from .enums import MouseButton
from .errors import MakcuConnectionError

# Version info
__version__ = "2.2.0"
__author__ = "SleepyTotem"

# Main exports
__all__ = [
    'MakcuController',
    'MouseButton',
    'MakcuConnectionError',
    'create_controller',
    'create_async_controller',
    'maybe_async'
]