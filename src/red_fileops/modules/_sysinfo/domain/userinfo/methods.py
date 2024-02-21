import platform

SYSTEM: str = platform.system().lower()

match SYSTEM:
    case "linux":
        from ._unix import get_groups, get_uuid as get_user_id
    case "windows":
        from ._win import get_groups, get_sid as get_user_id
    case _:
        raise ValueError(f"Unknown OS type: {SYSTEM}")
