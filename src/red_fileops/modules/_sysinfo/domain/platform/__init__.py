from __future__ import annotations

from . import methods, schemas, utils
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
from .schemas import (
    PlatformInfo,
    PlatformLinuxInfo,
    PlatformMacInfo,
    PlatformPython,
    PlatformUname,
    PlatformUnixInfo,
    PlatformWinInfo,
)
from .utils import print_platform

from red_fileops.modules._sysinfo.domain.enums.platform import (
    EnumLinux,
    EnumMac,
    EnumPlatform,
    EnumPython,
    EnumUname,
    EnumUnix,
    EnumWin32,
)
