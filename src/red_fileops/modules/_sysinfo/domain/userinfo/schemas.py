from __future__ import annotations

from dataclasses import dataclass, field
import os
from pathlib import Path
from typing import Union

from .methods import get_groups, get_user_id

from red_sysinfo.domain.mixins import DictMixin

@dataclass
class UserInfo(DictMixin):
    username: Path = field(default=Path.home().name)
    user_id: str = field(default_factory=get_user_id)
    groups: list = field(default_factory=get_groups)
    home: Path = field(default=Path.home())
    path: str = field(default=os.environ["PATH"])
