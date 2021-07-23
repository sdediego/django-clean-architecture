# coding: utf-8

from dataclasses import dataclass


@dataclass
class Currency:
    code: str
    name: str
    symbol: str

    def __str__(self) -> str:
        _symbol = f" ({self.symbol}):" if self.symbol else ":"
        return f'{self.code}{_symbol} {self.name}'
