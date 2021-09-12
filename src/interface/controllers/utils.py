# coding: utf-8

import operator
from functools import reduce

from src.domain.exchange_rate import CurrencyEntity


def calculate_time_weighted_rate(rate_series: list) -> float:
    return reduce(operator.mul, rate_series)**(1.0 / len(rate_series))


def filter_currencies(code: str, currencies: list) -> CurrencyEntity:
    currency = list(filter(
        lambda x: x.code == code if hasattr(x, 'code') else False, currencies))
    return currency[0] if len(currency) > 0 else None
