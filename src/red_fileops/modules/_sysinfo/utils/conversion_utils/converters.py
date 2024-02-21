from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Union

valid_units: list[str] = ["B", "KB", "MB", "GB", "TB", "PB"]


@dataclass
class ConvertedBytes:
    amount: Union[Decimal, int] = field(default=0.00)
    unit: str = field(default="B")

    def __post_init__(self):
        if self.unit not in valid_units:
            raise ValueError(f"Invalid unit: {self.unit}. Must be one of {valid_units}")

        round_amount: Decimal = round(self.amount, 2)
        self.amount = round_amount


def convert_bytes(
    bytes: int = None, as_obj: bool = False, as_str: bool = False
) -> Union[ConvertedBytes, str, int]:
    """Scale bytes up to proper unit (K, M, G, T, P).

    Params:
    -------

    bytes (int): Input bytes to convert up to proper unit.

    Example:
    -------
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    
    """
    if as_obj and as_str:
        raise ValueError(
            f"Cannot pass both as_obj=True and as_str=True. Please use only 1 or the other."
        )

    factor: int = 1024

    for unit in valid_units:
        if bytes < factor:
            if as_str:
                return f"{bytes:.2f}{unit}"
            elif as_obj:
                return ConvertedBytes(amount=Decimal(bytes), unit=unit)
            else:
                return round(bytes, 2)
        else:
            bytes /= factor
