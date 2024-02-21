from __future__ import annotations

from enum import Enum
import platform
from typing import NamedTuple, Tuple

class EnumMac(Enum):
    VERSION: Tuple[str] = platform.mac_ver()
