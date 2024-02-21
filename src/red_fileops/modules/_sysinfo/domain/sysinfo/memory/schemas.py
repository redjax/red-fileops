from typing import Any
from datetime import datetime
from dataclasses import dataclass, field

import psutil

from red_fileops.modules._sysinfo.domain.mixins import DictMixin


def ts_now() -> datetime:
    return datetime.now()


def get_vmem() -> "VirtualMemory":
    """Return an instance of platform-appropriate svmem (virtual memory)."""
    try:
        return VirtualMemory()
    except Exception as exc:
        raise Exception(f"Unhandled exception getting virtual memory. Details: {exc}")


def get_swap() -> "SwapMemory":
    """Return an instance of platform-appropriate swap memory."""
    try:
        return SwapMemory()
    except Exception as exc:
        raise Exception(f"Unhandled exception getting swap memory. Details: {exc}")


def get_memory_info() -> "MemoryInfo":
    """Return an instance of a compiled MemoryInfo class.

    This class has attributes with details about system's memory,
    based on a snapshot of virtual memory.
    """
    try:
        return MemoryInfo()
    except Exception as exc:
        raise Exception(f"Unhandled exception getting MemoryInfo class. Details: {exc}")


@dataclass
class VirtualMemory(DictMixin):
    """Snapshot system's virtual memory.

    This is the basis for memory checks like availability, total, etc.

    This class stores the initial generation of the virtual memory object,
    as well as its last refreshed time.
    """

    first_check: datetime = field(default_factory=ts_now)
    refreshed: datetime = field(default=None)
    snapshot: Any = field(default=None)

    def __post_init__(self):
        self.snapshot = psutil.virtual_memory()
        self.refreshed = ts_now()

    def get(self) -> Any:
        """Return a platform-compatible version of svmem object.

        smem object is a psutil platform-compatible virtual memory object."""
        if self.snapshot is None:
            self.snapshot = psutil.virtual_memory()
            self.refreshed = ts_now()

        return self.snapshot

    def refresh(self) -> Any:
        """Refresh the memory snapshot.

        This allows for updating the .refreshed value, while leaving .first_check intact.
        """
        self.snapshot = psutil.virtual_memory()
        self.refreshed = ts_now()

        return self.snapshot


@dataclass
class SwapMemory(DictMixin):
    """Snapshot system's swap memory.

    This is the basis for memory checks like swap availability, total, etc.

    This class stores the initial generation of the swap memory object,
    as well as its last refreshed time.
    """

    first_check: datetime = field(default_factory=ts_now)
    refreshed: datetime = field(default=None)
    snapshot: Any = field(default=None)

    def __post_init__(self):
        self.snapshot = psutil.swap_memory()
        self.refreshed = ts_now()

    def get(self) -> Any:
        """Return a platform-compatible version of swap object.

        smem object is a psutil platform-compatible virtual memory object."""
        if self.snapshot is None:
            self.snapshot = psutil.swap_memory()
            self.refreshed = ts_now()

        return self.snapshot

    def refresh(self) -> Any:
        """Refresh the memory snapshot.

        This allows for updating the .refreshed value, while leaving .first_check intact.
        """
        self.snapshot = psutil.swap_memory()
        self.refreshed = ts_now()

        return self.snapshot


@dataclass
class SnapshotDetail(DictMixin):
    vmem_snapshot_created: datetime = field(default=None)
    vmem_snapshot_refreshed: datetime = field(default=None)
    swap_snapshot_created: datetime = field(default=None)
    swap_snapshot_refreshed: datetime = field(default=None)


@dataclass
class MemoryInfoBase(DictMixin):
    vmem: VirtualMemory = field(default_factory=get_vmem)
    swap: SwapMemory = field(default_factory=get_swap)

    @property
    def snapshots(self) -> SnapshotDetail:
        detail: SnapshotDetail = SnapshotDetail(
            vmem_snapshot_created=self.vmem.first_check,
            vmem_snapshot_refreshed=self.vmem.refreshed,
            swap_snapshot_created=self.swap.first_check,
            swap_snapshot_refreshed=self.swap.refreshed,
        )

        return detail

    @property
    def snapshot(self) -> Any:
        return self.vmem.snapshot

    @property
    def last_refresh(self) -> datetime:
        return self.vmem.refreshed

    def __post_init__(self):
        pass


@dataclass
class MemoryInfo(MemoryInfoBase):
    total: int = field(default=0)
    available: int = field(default=0)
    percent: float = field(default=0.0)
    used: int = field(default=0)
    free: int = field(default=0)
    active: int = field(default=0)
    inactive: int = field(default=0)
    buffers: int = field(default=0)
    cached: int = field(default=0)
    shared: int = field(default=0)
    slab: int = field(default=0)

    def __post_init__(self):
        self.total = self.vmem.snapshot.total
        self.available = self.vmem.snapshot.available
        self.percent = self.vmem.snapshot.percent
        self.used = self.vmem.snapshot.used
        self.free = self.vmem.snapshot.free
        self.active = self.vmem.snapshot.active
        self.inactive = self.vmem.snapshot.inactive
        self.buffers = self.vmem.snapshot.buffers
        self.cached = self.vmem.snapshot.cached
        self.shared = self.vmem.snapshot.shared
        self.slab = self.vmem.snapshot.slab

    def refresh(self) -> None:
        self.vmem.refresh()
