class MakcuError(Exception):
    """Base exception for all Makcu-related errors."""
    pass

class MakcuConnectionError(MakcuError):
    """Raised when the device connection fails."""
    pass

class MakcuCommandError(MakcuError):
    """Raised when a device command is invalid, rejected, or fails."""
    pass

class MakcuTimeoutError(MakcuError):
    """Raised when the device does not respond in time."""
    pass

class MakcuResponseError(MakcuError):
    """Raised when the response from the device is malformed or unexpected."""
    pass