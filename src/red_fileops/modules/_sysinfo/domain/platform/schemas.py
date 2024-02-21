from __future__ import annotations

from dataclasses import asdict, dataclass, field
from types import ModuleType
from typing import Any, Tuple, Union

from red_fileops.modules._sysinfo.domain.enums.platform import (
    EnumLinux,
    EnumMac,
    EnumPlatform,
    EnumPython,
    EnumSystemTypes,
    EnumUname,
    EnumUnix,
    EnumWin32,
)
from red_fileops.modules._sysinfo.domain.mixins import DictMixin

from .methods import (
    get_python_base_prefix,
    get_python_copyright,
    get_python_default_encoding,
    get_python_exec_prefix,
    get_python_executable,
    get_python_flags,
    get_python_float_info,
    get_python_max_int_digits,
    get_python_maxsize,
    get_python_maxunicode,
    get_python_modules,
    get_python_path,
    get_python_recursion_limit,
    get_python_suppress_bytecode,
    get_sys_byteorder,
)


def get_platform_uname() -> "PlatformUname":
    """Return an initalized PlatformUname instance."""
    _uname: PlatformUname = PlatformUname()

    return _uname


def get_platform_python() -> "PlatformPython":
    """Return an initalized PlatformPython instance."""
    _python: PlatformPython = PlatformPython()

    return _python


@dataclass
class PlatformUname(DictMixin):
    system: str = field(default=EnumUname.SYSTEM.value)
    node: str = field(default=EnumUname.NODE.value)
    release: str = field(default=EnumUname.RELEASE.value)
    version: str = field(default=EnumUname.VERSION.value)
    machine: str = field(default=EnumUname.MACHINE.value)


@dataclass
class PlatformPython(DictMixin):
    """Information about the Python implementation for the platform."""

    build: Tuple[str, str] = EnumPython.BUILD.value
    compiler: str = EnumPython.COMPILER.value
    branch: str = EnumPython.BRANCH.value
    implementation: str = EnumPython.IMPLEMENTATION.value
    revision: str = EnumPython.REVISION.value
    version: str = EnumPython.VERSION.value
    version_tuple: Tuple[str, str, str] = EnumPython.VERSION_TUPLE.value
    path: list[str] = field(default_factory=get_python_path)
    modules: list[ModuleType] = field(default_factory=get_python_modules)
    base_prefix: str = field(default_factory=get_python_base_prefix)
    exec_prefix: str = field(default_factory=get_python_exec_prefix)
    copyright: str = field(default_factory=get_python_copyright)
    dont_write_bytecode: bool = field(default_factory=get_python_suppress_bytecode)
    executable: str = field(default_factory=get_python_executable)
    flags: tuple[Union[int, bool]] = field(default_factory=get_python_flags)
    float_info: tuple[Union[int, float]] = field(default_factory=get_python_float_info)
    default_encoding: str = field(default_factory=get_python_default_encoding)
    int_max_str_digits: int = field(default_factory=get_python_max_int_digits)
    recursion_limit: int = field(default_factory=get_python_recursion_limit)
    maxsize: int = field(default_factory=get_python_maxsize)
    maxunicode: int = field(default_factory=get_python_maxunicode)


@dataclass
class PlatformInfoBase(DictMixin):
    """Store cross-platform information gleaned from platform module.

    Platform-specific functionality is implemented in Platform<x> children,
    i.e. PlatformWindowsInfo.

    The parameters in this class are initialized from PlatformEnum by default.
    """

    platform: str = field(default=EnumPlatform.PLATFORM.value)
    platform_terse: str = field(default=EnumPlatform.PLATFORM_TERSE.value)
    platform_aliased: str = field(default=EnumPlatform.PLATFORM_ALIASED.value)
    machine: str = field(default=EnumPlatform.MACHINE.value)
    system: str = field(default=EnumPlatform.SYSTEM.value)
    release: str = field(default=EnumPlatform.RELEASE.value)
    version: str = field(default=EnumPlatform.VERSION.value)
    processor: str | None = field(default=EnumPlatform.PROCESSOR.value)
    arch: tuple[str, str] = field(default=EnumPlatform.ARCH.value)
    uname: PlatformUname = field(default_factory=get_platform_uname)
    python: PlatformPython = field(default_factory=get_platform_python)
    byteorder: str = field(default_factory=get_sys_byteorder)

    def is_linux(self) -> bool:
        if self.system == EnumSystemTypes.LINUX.value:
            return True
        else:
            return False

    def is_unix(self) -> bool:
        if self.system in [EnumSystemTypes.LINUX.value, EnumSystemTypes.MAC.value]:
            return True
        else:
            return False

    def is_win(self) -> bool:
        if self.system == EnumSystemTypes.WINDOWS.value:
            return True
        else:
            return False

    def is_mac(self) -> bool:
        if self.system == EnumSystemTypes.MAC.value:
            return True
        else:
            return False

    def is_java(self) -> bool:
        if self.system == EnumSystemTypes.JAVA.value:
            return True
        else:
            return False

    def is_32bit(self) -> bool:
        if "32bit" in self.arch:
            return True
        else:
            return False

    def is_64bit(self) -> bool:
        if "64bit" in self.arch:
            return True
        else:
            return False


@dataclass
class PlatformInfo(PlatformInfoBase):
    pass


@dataclass
class PlatformWinInfo(PlatformInfoBase):
    """Windows-specific platform info."""

    win32_ver: Tuple = field(default=EnumWin32.VERSION.value)
    win32_edition: str = field(default=EnumWin32.EDITION.value)
    win32_is_iot: bool = field(default=EnumWin32.IS_IOT.value)


@dataclass
class PlatformMacInfo(PlatformInfoBase):
    """Mac-specific platform info."""

    mac_ver: Tuple[str] = field(default=EnumMac.VERSION.value)


@dataclass
class PlatformUnixInfo(PlatformInfoBase):
    libc_ver: Tuple[str] = field(default=EnumUnix.LIBC_VER.value)


@dataclass
class PlatformLinuxInfo(PlatformInfoBase):
    os_release: dict[str, str] = field(default_factory=EnumLinux.OS_RELEASE.value)
