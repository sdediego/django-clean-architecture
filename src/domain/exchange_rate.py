# coding: utf-8

from dataclasses import dataclass
from datetime import date


@dataclass
class CurrencyEntity:
    code: str
    name: str
    symbol: str

    def __str__(self) -> str:
        _symbol = f" ({self.symbol}):" if self.symbol else ":"
        return f'{self.code}{_symbol} {self.name}'


@dataclass
class CurrencyExchangeRateEntity:
    source_currency: CurrencyEntity
    exchanged_currency: CurrencyEntity
    valuation_date: date
    rate_value: float

    def __str__(self) -> str:
        source_currency = self.source_currency.code
        exchanged_currency = self.exchanged_currency.code
        return (
            f'{source_currency}/{exchanged_currency} '
            f'= {self.rate_value} ({self.valuation_date})'
        )

    def calculate_amount(self, amount: float) -> float:
        return round(amount * self.rate_value, 2)
