from datetime import datetime
import psutil


def get_last_boot() -> datetime:
    """Get the time of last system boot."""
    last_boot: datetime.fromtimestamp(psutil.boot_time())

    return last_boot
