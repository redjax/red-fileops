from typing import Union
from dataclasses import dataclass, field
from pathlib import Path
import os

from red_sysinfo.domain.mixins import DictMixin
from .methods import get_user_id, get_groups


@dataclass
class UserInfo(DictMixin):
    username: Path = field(default=Path.home().name)
    user_id: str = field(default_factory=get_user_id)
    groups: list = field(default_factory=get_groups)
    home: Path = field(default=Path.home())
    path: str = field(default=os.environ["PATH"])
