# coding: utf-8

import operator
from functools import reduce
from typing import List

from src.domain.exchange_rate import (
    CurrencyEntity, CurrencyExchangeAmountEntity, CurrencyExchangeRateEntity,
    TimeWeightedRateEntity)


def calculate_time_weighted_rate(rate_series: list) -> TimeWeightedRateEntity:
    twr = reduce(operator.mul, rate_series)**(1.0 / len(rate_series))
    return TimeWeightedRateEntity(time_weighted_rate=twr)


def calculate_exchanged_amount(exchange_rate: CurrencyExchangeRateEntity,
                               amount: float) -> CurrencyExchangeAmountEntity:
    return CurrencyExchangeAmountEntity(
        exchanged_currency=exchange_rate.exchanged_currency,
        exchanged_amount=exchange_rate.calculate_amount(amount),
        rate_value=exchange_rate.rate_value
    )


def filter_currencies(code: str, currencies: list) -> CurrencyEntity:
    currency = list(filter(
        lambda x: x.code == code if hasattr(x, 'code') else False, currencies))
    return currency[0] if len(currency) > 0 else None


def get_rate_series(timeseries: list) -> List[float]:
    return list(map(lambda x: round(x.rate_value, 6), timeseries))
