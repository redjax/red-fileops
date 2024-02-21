from __future__ import annotations

import sys
from types import ModuleType
from typing import Union

def get_sys_byteorder() -> str:
    """Return "big" or "little.

    "big" for big-endian (most-significant byte first) platforms.
    "little" on little-endian (least-significant byte first) platforms.
    """
    return sys.byteorder


def get_python_path() -> list[str]:
    """Return paths Python interpreter is aware of."""
    return sys.path


def get_python_modules() -> dict[str, ModuleType]:
    """Return dict of modules Python is aware of."""
    return sys.modules


def get_python_base_prefix() -> str:
    """Return Python's base prefix."""
    return sys.base_prefix


def get_python_exec_prefix() -> str:
    """Return Python's platform-dependent install files are. By default, this is /usr/local."""
    return sys.exec_prefix


def get_python_executable() -> str:
    """Return path to Python's executable file."""
    return sys.executable


def get_python_copyright() -> str:
    """Return Python interpreter's copyright statement."""
    return sys.copyright


def get_python_suppress_bytecode() -> bool:
    """Return value of PYTHONDONTWRITEBYTECODE.

    If value is False, Python will write .pyc files.
    If value is True, Python will not write .pyc files.
    """
    return sys.dont_write_bytecode


def get_python_flags() -> tuple[Union[int, bool]]:
    """Return status of Python CLI flags."""
    return sys.flags


def get_python_float_info() -> tuple[Union[int, float]]:
    """Return information about platform's float type.

    Contains low-level information about precision & internal representation.
    """
    return sys.float_info


def get_python_default_encoding() -> str:
    """Return environment's default encoding parameter. Default value is 'utf-8.'."""
    return sys.getdefaultencoding()


def get_python_max_int_digits() -> int:
    """Return the integer string conversion length limit."""
    return sys.get_int_max_str_digits()


def get_python_recursion_limit() -> int:
    """Return maximum Python interpreter call stack depth.

    Prevents recursion from causing a stack overflow.
    """
    return sys.getrecursionlimit()


def get_python_maxsize() -> int:
    """Maximum size of an individual veriable/object.

    For 32-bit, value is normally 2**31 - 1.
    For 64-bit, value is normally 2**64 - 1.
    """
    return sys.maxsize


def get_python_maxunicode() -> int:
    """Integer giving value of the largest Unicode code point."""
    return sys.maxunicode
