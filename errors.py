class MakcuError(Exception):
    pass

class MakcuConnectionError(MakcuError):
    pass

class MakcuCommandError(MakcuError):
    pass

class MakcuTimeoutError(MakcuError):
    pass

class MakcuResponseError(MakcuError):
    pass