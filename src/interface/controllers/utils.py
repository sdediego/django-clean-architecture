# coding: utf-8

import operator
from functools import reduce


def calculate_time_weighted_rate(rate_series: list) -> float:
    return reduce(operator.mul, rate_series)**(1.0 / len(rate_series))
