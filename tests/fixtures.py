# coding: utf-8

import datetime
import random

import pytest

from src.domain.exchange_rate import CurrencyEntity, CurrencyExchangeRateEntity


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
def currency_exchange_rate(currency) -> CurrencyExchangeRateEntity:
    return CurrencyExchangeRateEntity(
        source_currency=currency.code,
        exchanged_currency='GBP',
        valuation_date=datetime.date.today().strftime('%Y-%m-%d'),
        rate_value=random.uniform(0.75, 1.5)
    )
