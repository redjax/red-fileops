from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import NamedTuple, Tuple

import psutil
from psutil._common import scpufreq

class EnumBasicSysInfo(Enum):
    LAST_BOOT: datetime = datetime.fromtimestamp(psutil.boot_time())


class EnumCPUCores(Enum):
    PHYSICAL: int = psutil.cpu_count(logical=False)
    TOTAL: int = psutil.cpu_count(logical=True)
