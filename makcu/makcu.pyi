from typing import Optional, Dict, Callable, List, Union
from .controller import MakcuController
from .enums import MouseButton
from .errors import MakcuError, MakcuConnectionError, MakcuCommandError, MakcuTimeoutError, MakcuResponseError

__version__: str
__all__: List[str]

def create_controller(
    fallback_com_port: str = "", 
    debug: bool = False, 
    send_init: bool = True
) -> MakcuController: ...