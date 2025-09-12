from typing import List
from .controller import MakcuController

__version__: str
__all__: List[str]

def create_controller(
    fallback_com_port: str = "", 
    debug: bool = False, 
    send_init: bool = True
) -> MakcuController: ...