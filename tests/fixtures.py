# coding: utf-8

import datetime
import random
import string

import pytest

from src.domain.core.constants import HTTP_VERBS
from src.domain.core.routing import Route, Router
from src.domain.exchange_rate import (
    CurrencyEntity, CurrencyExchangeRateEntity,
    CurrencyExchangeAmountEntity, TimeWeightedRateEntity)
from src.domain.constants import (
    BOOLEAN_SETTING_TYPE, FLOAT_SETTING_TYPE, INTEGER_SETTING_TYPE,
    SECRET_SETTING_TYPE, TEXT_SETTING_TYPE, URL_SETTING_TYPE)
from src.domain.provider import ProviderEntity, ProviderSettingEntity
from src.infrastructure.clients.provider.utils import get_drivers_names


def generate_random_string(size: int) -> str:
    return ''.join([random.choice(string.ascii_letters) for _ in range(size)])


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


@pytest.fixture
def provider() -> ProviderEntity:
    name = generate_random_string(10)
    return ProviderEntity(
        name=name,
        driver=random.choice(get_drivers_names()),
        priority=random.randint(1, 9),
        enabled=random.choice([True, False]),
        settings=dict()
    )


@pytest.fixture
def provider_setting(provider) -> ProviderSettingEntity:
    setting_type, value = random.choice([
        (BOOLEAN_SETTING_TYPE, random.choice(['True', 'False'])),
        (INTEGER_SETTING_TYPE, random.randint(1, 99)),
        (FLOAT_SETTING_TYPE, random.uniform(1.00, 99.99)),
        (SECRET_SETTING_TYPE, ProviderSettingEntity.encode_secret('secret')),
        (TEXT_SETTING_TYPE, generate_random_string(10)),
        (URL_SETTING_TYPE, generate_random_string(10)),
    ])
    return ProviderSettingEntity(
        provider=provider,
        setting_type=setting_type,
        key=generate_random_string(10),
        value=value,
        description=generate_random_string(25)
    )


@pytest.fixture
def route() -> Route:

    class TestController:
        def test_method(self) -> str:
            return 'test_method'

    return Route(
        http_verb=random.choice(list(HTTP_VERBS)),
        path='/api/path/to/fake/endpoint/',
        controller=TestController,
        method='test_method',
        name='test_route',
    )


@pytest.fixture
def router(route) -> Router:
    router = Router()
    router.register(route)
    return router
