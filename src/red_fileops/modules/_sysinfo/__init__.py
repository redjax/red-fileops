from __future__ import annotations

from . import domain
from .domain.platform.schemas import PlatformInfo
from .domain.platform.utils import print_platform
from .utils.platform_utils import get_platform

PLATFORM: PlatformInfo = PlatformInfo()
