from __future__ import annotations

from .utils.platform_utils import get_platform

from . import domain
from .domain.platform.schemas import PlatformInfo
from .domain.platform.utils import print_platform

PLATFORM: PlatformInfo = PlatformInfo()
