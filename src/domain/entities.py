# coding: utf-8

from dataclasses import dataclass
from datetime import date


@dataclass
class Currency:
    code: str
    name: str
    symbol: str

    def __str__(self) -> str:
        _symbol = f" ({self.symbol}):" if self.symbol else ":"
        return f'{self.code}{_symbol} {self.name}'


@dataclass
class CurrencyExchangeRate:
    source_currency: Currency
    exchanged_currency: Currency
    valuation_date: date
    rate_value: float

    def __str__(self) -> str:
        source_currency = self.source_currency.code
        exchanged_currency = self.exchanged_currency.code
        return (
            f'{source_currency}/{exchanged_currency} '
            f'= {self.rate_value} ({self.valuation_date})'
        )
