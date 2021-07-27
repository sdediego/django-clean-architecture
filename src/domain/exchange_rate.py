# coding: utf-8

from dataclasses import dataclass
from datetime import date


@dataclass
class CurrencyEntity:
    code: str
    name: str
    symbol: str

    @staticmethod
    def to_string(currency: 'CurrencyEntity') -> str:
        symbol = f" ({currency.symbol}):" if currency.symbol else ":"
        return f'{currency.code}{symbol} {currency.name}'


@dataclass
class CurrencyExchangeRateEntity:
    source_currency: CurrencyEntity
    exchanged_currency: CurrencyEntity
    valuation_date: date
    rate_value: float

    @staticmethod
    def to_string(exchange_rate: 'CurrencyExchangeRateEntity') -> str:
        source_currency = exchange_rate.source_currency.code
        exchanged_currency = exchange_rate.exchanged_currency.code
        return (
            f'{source_currency}/{exchanged_currency} '
            f'= {exchange_rate.rate_value} ({exchange_rate.valuation_date})'
        )

    def calculate_amount(self, amount: float) -> float:
        return round(amount * self.rate_value, 2)
