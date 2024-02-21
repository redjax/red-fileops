from __future__ import annotations

from typing import Any, Union

from dataclasses import asdict, dataclass, field
from datetime import datetime

from red_fileops.modules._sysinfo.domain.mixins import DictMixin
from red_fileops.modules._sysinfo.domain.enums.sysinfo import EnumCPUCores, EnumBasicSysInfo
from red_fileops.modules._sysinfo.utils.conversion_utils import convert_bytes

import psutil

from .methods import get_last_boot

from .cpu import CPUInfo, get_cpu_info
from .memory import MemoryInfo, get_memory_info


@dataclass
class SystemInfoBase(DictMixin):
    """Store system information gleaned from psutil module."""

    last_boot: datetime = field(default=EnumBasicSysInfo.LAST_BOOT.value)
    cpu: CPUInfo = field(default_factory=get_cpu_info)
    memory: MemoryInfo = field(default_factory=get_memory_info)
    # disk
    # network


@dataclass
class SystemInfo(SystemInfoBase):
    pass
