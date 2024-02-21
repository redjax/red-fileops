from enum import Enum
import psutil
from psutil._common import scpufreq

from typing import NamedTuple, Tuple
from datetime import datetime


class EnumBasicSysInfo(Enum):
    LAST_BOOT: datetime = datetime.fromtimestamp(psutil.boot_time())


class EnumCPUCores(Enum):
    PHYSICAL: int = psutil.cpu_count(logical=False)
    TOTAL: int = psutil.cpu_count(logical=True)
