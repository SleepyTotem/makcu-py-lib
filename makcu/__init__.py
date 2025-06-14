from typing import List
from .controller import MakcuController, create_controller, create_async_controller
from .enums import MouseButton
from .errors import (
    MakcuError, 
    MakcuConnectionError, 
    MakcuCommandError,
    MakcuTimeoutError,
    MakcuResponseError
)

__version__: str = "2.0.0"
__author__: str = "SleepyTotem"
__license__: str = "GPL"

__all__: List[str] = [
    "MakcuController",
    "create_controller",
    "create_async_controller",
    "MouseButton",
    "MakcuError",
    "MakcuConnectionError",
    "MakcuCommandError", 
    "MakcuTimeoutError",
    "MakcuResponseError",
]

from .controller import MakcuController as Controller

__doc__ = """
Makcu Python Library provides a high-performance interface for controlling
Makcu USB devices. Features include:

- Full async/await support for modern Python applications
- Zero-delay command execution with intelligent tracking
- Automatic device reconnection on disconnect
- Human-like mouse movement and clicking patterns
- Comprehensive button and axis locking
- Real-time button event monitoring

Quick Start:
    >>> from makcu import create_controller, MouseButton
    >>> makcu = create_controller()
    >>> makcu.click(MouseButton.LEFT)
    >>> makcu.move(100, 50)
    >>> makcu.disconnect()

Async Usage:
    >>> import asyncio
    >>> from makcu import create_async_controller, MouseButton
    >>> 
    >>> async def main():
    ...     async with await create_async_controller() as makcu:
    ...         await makcu.click(MouseButton.LEFT)
    ...         await makcu.move(100, 50)
    >>> 
    >>> asyncio.run(main())

For more information, visit: https://github.com/SleepyTotem/makcu-py-lib
"""