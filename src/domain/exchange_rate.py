# coding: utf-8

from dataclasses import dataclass
from datetime import date
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
    valuation_date: str = None
    rate_value: float = None

    def __post_init__(self):
        if self.valuation_date and isinstance(self.valuation_date, date):
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


@dataclass
class CurrencyExchangeAmountEntity:
    exchanged_currency: str = None
    exchanged_amount: float = None
    rate_value: float = None

    def __post_init__(self):
        if hasattr(self.exchanged_currency, 'code'):
            self.exchanged_currency = self.exchanged_currency.code
        if self.exchanged_amount:
            self.exchanged_amount = round(float(self.exchanged_amount), 2)
        if self.rate_value:
            self.rate_value = round(float(self.rate_value), 6)

    @staticmethod
    def to_string(exchange_amount: 'CurrencyExchangeAmountEntity') -> str:
        return (
            f'{exchange_amount.exchanged_currency}({exchange_amount.rate_value})'
            f' = {exchange_amount.exchanged_amount}'
        )


@dataclass
class TimeWeightedRateEntity:
    time_weighted_rate: float = None

    def __post_init__(self):
        if self.time_weighted_rate:
            self.time_weighted_rate = round(float(self.time_weighted_rate), 6)

    @staticmethod
    def to_string(time_weighted_rate: 'TimeWeightedRateEntity') -> str:
        return f'twr = {time_weighted_rate.time_weighted_rate}'
