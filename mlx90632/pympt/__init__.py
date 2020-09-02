from mlx90632.pympt.core import *
from mlx90632.pympt.channel import MptChannel

import sys

__all__ = ["MptException", "BadCrcException", "CommandTooLongException",
           "NotConnectedException", "I2CAcknowledgeError", "MptChannel"]

if sys.platform == "Linux":
    from mlx90632.pympt.UsbHidChannel import UsbHidChannel
    __all__.append("UsbHidChannel")
else:
    from mlx90632.pympt.PyWinUsbChannel import PyWinUsbChannel
    __all__.append("PyWinUsbChannel")
