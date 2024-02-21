from __future__ import annotations

from enum import Enum
import platform
from typing import NamedTuple, Tuple

class EnumWin32(Enum):
    VERSION: Tuple[str] = platform.win32_ver()
    EDITION: str = platform.win32_edition()
    IS_IOT: bool = platform.win32_is_iot()
