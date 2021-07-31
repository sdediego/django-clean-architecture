# coding: utf-8

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Union


@dataclass
class CurrencyEntity:
    code: str = None
    name: str = None
    symbol: str = None

    @staticmethod
    def to_string(currency: 'CurrencyEntity') -> str:
        symbol = f" ({currency.symbol}):" if currency.symbol else ":"
        return f'{currency.code}{symbol} {currency.name}'


@dataclass
class CurrencyExchangeRateEntity:
    source_currency: Union[CurrencyEntity, str] = None
    exchanged_currency: Union[CurrencyEntity, str] = None
    valuation_date: Union[date, str] = None
    rate_value: Union[Decimal, float] = None

    def __post_init__(self):
        if self.valuation_date and not isinstance(self.valuation_date, str):
            self.valuation_date = self.valuation_date.strftime('%Y-%m-%d')
        if self.rate_value:
            self.rate_value = round(float(self.rate_value), 6)

    @staticmethod
    def to_string(exchange_rate: 'CurrencyExchangeRateEntity') -> str:
        source_currency = exchange_rate.source_currency.code if hasattr(
            exchange_rate.source_currency, 'code') else exchange_rate.source_currency
        exchanged_currency = exchange_rate.exchanged_currency.code if hasattr(
            exchange_rate.exchanged_currency, 'code') else exchange_rate.exchanged_currency
        return (
            f'{source_currency}/{exchanged_currency} '
            f'= {exchange_rate.rate_value} ({exchange_rate.valuation_date})'
        )

    def calculate_amount(self, amount: float) -> float:
        return round(amount * self.rate_value, 2)
