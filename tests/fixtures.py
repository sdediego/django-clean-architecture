# coding: utf-8

import datetime
import random

import pytest

from src.domain.exchange_rate import (
    CurrencyEntity, CurrencyExchangeRateEntity,
    CurrencyExchangeAmountEntity, TimeWeightedRateEntity)


@pytest.fixture
def currency() -> CurrencyEntity:
    currency_attrs = random.choice([
        {
            'code': 'EUR',
            'name': 'Euro',
            'symbol': '€'
        },
        {
            'code': 'USD',
            'name': 'US Dollar',
            'symbol': '$'
        }
    ])
    return CurrencyEntity(
        code=currency_attrs.get('code'),
        name=currency_attrs.get('name'),
        symbol=currency_attrs.get('symbol')
    )


@pytest.fixture
def exchange_rate(currency) -> CurrencyExchangeRateEntity:
    return CurrencyExchangeRateEntity(
        source_currency=currency.code,
        exchanged_currency='GBP',
        valuation_date=datetime.date.today().strftime('%Y-%m-%d'),
        rate_value=round(random.uniform(0.75, 1.5), 6)
    )


@pytest.fixture
def exchange_amount(exchange_rate) -> CurrencyExchangeAmountEntity:
    return CurrencyExchangeAmountEntity(
        exchanged_currency=exchange_rate.exchanged_currency,
        exchanged_amount=round(random.uniform(10, 100), 2),
        rate_value=exchange_rate.rate_value
    )


@pytest.fixture
def time_weighted_rate() -> TimeWeightedRateEntity:
    return TimeWeightedRateEntity(
        time_weighted_rate=round(random.uniform(0.75, 1.5), 6)
    )
