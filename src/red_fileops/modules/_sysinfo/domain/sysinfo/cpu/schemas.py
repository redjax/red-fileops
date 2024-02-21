from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from red_fileops.modules._sysinfo.domain.enums.sysinfo import EnumCPUCores
from red_fileops.modules._sysinfo.domain.mixins import DictMixin

import psutil

def get_cpu_info() -> "CPUInfo":
    """Get CPU core info."""
    physical = EnumCPUCores.PHYSICAL.value
    total = EnumCPUCores.TOTAL.value

    # return {"physical": physical, "total": total}
    return CPUInfo(physical_cores=physical, total_cores=total)


@dataclass
class CPUFrequency(DictMixin):
    last_updated: datetime = field(default=datetime.now())
    current: str = field(default=None)
    min: str = field(default=None)
    max: str = field(default=None)


@dataclass
class CPUCore(DictMixin):
    last_updated: datetime = field(default=datetime.now())
    core_num: int = field(default=0)
    usage: float = field(default=0.0)


@dataclass
class CPUCoreUsage(DictMixin):
    cores: list[CPUCore] = field(default=None)


@dataclass
class CPUInfo(DictMixin):
    physical_cores: int = field(default=EnumCPUCores.PHYSICAL.value)
    total_cores: int = field(default=EnumCPUCores.TOTAL.value)

    def frequency(self) -> CPUFrequency:
        cpu_freq = psutil.cpu_freq()

        min: str = f"{cpu_freq.min:.2f}Mhz"
        max: str = f"{cpu_freq.max:.2f}Mhz"
        current: str = f"{cpu_freq.current:.2f}Mhz"

        return_obj: CPUFrequency = CPUFrequency(current=current, min=min, max=max)

        return return_obj

    def core_usage(self) -> CPUCoreUsage:
        _cores: list[CPUCore] = []

        for i, percent in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            core: CPUCore = CPUCore(core_num=i, usage=percent)
            _cores.append(core)

        return_obj: CPUCoreUsage = CPUCoreUsage(cores=_cores)

        return return_obj
