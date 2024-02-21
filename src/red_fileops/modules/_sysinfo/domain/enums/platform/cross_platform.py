from __future__ import annotations

from enum import Enum
import platform
from typing import NamedTuple, Tuple

class EnumPlatform(Enum):
    """Enumerate platform module outputs.

    Usage:
    ------

    Call enums by name, i.e. to get the system platform, call
    'EnumPlatform.PLATFORM'.

    Enumerations have 'name' and 'value' properties. The 'name' property
    simply returns the name of the enum (i.e. 'PLATFORM'), where the value
    will return the enumeration (i.e. 'Linux-5.10.0-26-amd64-x86_64-with-glibc2.31').

    Enums:
    ------

    - PLATFORM
        - value: platform.platform()
    - PLATFORM_TERSE
        - value: platform.platform(terse=True)
    - PLATFORM_ALIASED
        - value: platform.platform(aliased=True)
    - SYSTEM
        - value: platform.system()
    - RELEASE
        - value: platform.release()
    - VERSION
        - value: platform.version()
    - ARCH
        - value: platform.architecture()
    - UNAME:
        - value: platform.uname()
    """

    PLATFORM: str = platform.platform()
    PLATFORM_TERSE: str = platform.platform(terse=True)
    PLATFORM_ALIASED: str = platform.platform(aliased=True)
    MACHINE: str = platform.machine()
    SYSTEM: str = platform.system()
    RELEASE: str = platform.release()
    VERSION: str = platform.version()
    PROCESSOR: str = platform.processor()
    ARCH: tuple[str, str] = platform.architecture()
    UNAME: NamedTuple = platform.uname()


class EnumUname(Enum):
    """Enumerate platform.uname() properties.

    Usage:
    ------

    Call enums by name, i.e. to get uname().node, call
    'EnumUname.NODE'.

    Enumerations have 'name' and 'value' properties. The 'name' property
    simply returns the name of the enum (i.e. 'SYSTEM'), where the value
    will return the enumeration (i.e. 'Linux').

    Enums:
    ------

    - SYSTEM
        - value: platform.uname().system
    - NODE
        - value: platform.uname().node
    - RELEASE
        - value: platform.uname().release
    - VERSION
        - value: platform.uname().version
    - MACHINE
        - value: platform.uname().machine
    """

    SYSTEM: str = platform.uname().system
    NODE: str = platform.uname().node
    RELEASE: str = platform.uname().release
    VERSION: str = platform.uname().version
    MACHINE: str = platform.uname().machine


class EnumPython(Enum):
    """Enumerate platform.uname() properties.

    Usage:
    ------

    Call enums by name, i.e. to get uname().node, call
    'EnumUname.NODE'.

    Enumerations have 'name' and 'value' properties. The 'name' property
    simply returns the name of the enum (i.e. 'SYSTEM'), where the value
    will return the enumeration (i.e. 'Linux').

    Enums:
    ------

    - BRANCH
        - value: platform.python_branch()
    - BUILD
        - value: platform.python_build()
    - COMPILER
        - value: platform.python_compiler()
    - IMPLEMENTATION
        - value: platform.python_implementation()
    - REVISION
        - value: platform.python_revision()
    - VERSION
        - value: platform.python_version()
    - VERSION_TUPLE
        - value: platform.python_version_tuple()
    """

    BRANCH: str = platform.python_branch()
    BUILD: Tuple[str, str] = platform.python_build()
    COMPILER: str = platform.python_compiler()
    IMPLEMENTATION: str = platform.python_implementation()
    REVISION: str = platform.python_revision()
    VERSION: str = platform.python_version()
    VERSION_TUPLE: Tuple[str, str, str] = platform.python_version_tuple()


class EnumSystemTypes(Enum):
    """Enumerate options for platform.uname().system."""

    LINUX: str = "Linux"
    MAC: str = "Darwin"
    WINDOWS: str = "Windows"
    JAVA: str = "Java"
