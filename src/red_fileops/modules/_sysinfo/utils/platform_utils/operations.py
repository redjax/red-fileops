from __future__ import annotations

from red_fileops.modules._sysinfo.domain.platform import PlatformInfo

def get_platform() -> PlatformInfo:
    """Return an instance of PlatformInfo.

    This is the generic, cross-platform object with information read from the system
    the PlatformInfo object is initialized on.
    """
    try:
        PLATFORM = PlatformInfo()

        return PLATFORM

    except Exception as exc:
        raise Exception(
            f"Unhandled exception getting PlatformInfo object. Details: {exc}"
        )
