# coding: utf-8

import dataclasses
import json
import random

import pytest

from src.domain.exchange_rate import CurrencyEntity, CurrencyExchangeRateEntity
from src.infrastructure.orm.db.exchange_rate.models import (
    Currency, CurrencyExchangeRate)
from src.infrastructure.orm.db.exchange_rate.tasks import (
    bulk_save_currencies, bulk_save_exchange_rates, save_currency, save_exchange_rate)
from tests.fixtures import currency, exchange_rate
from tests.infrastructure.orm.db.factories.exchange_rate import (
    CurrencyFactory, CurrencyExchangeRateFactory)


@pytest.mark.django_db
def test_save_currency_task(currency):
    currency_json = json.dumps(dataclasses.asdict(currency))
    result = save_currency(currency_json)
    assert result is None
    assert Currency.objects.count() == 1


@pytest.mark.django_db
def test_save_exchange_rate_task(exchange_rate):
    exchange_rate_json = json.dumps(dataclasses.asdict(exchange_rate))
    result = save_exchange_rate(exchange_rate_json)
    assert result is None
    assert CurrencyExchangeRate.objects.count() == 1


@pytest.mark.django_db
def test_bulk_save_currencies_task():
    num_of_currencies = random.randint(1, 10)
    currencies = [
        CurrencyEntity(**{
            field: value for field, value in currency.__dict__.items() \
                if not field.startswith('_')
        })
        for currency in CurrencyFactory.build_batch(num_of_currencies)
    ]
    currencies_json = json.dumps(list(map(dataclasses.asdict, currencies)))
    result = bulk_save_currencies(currencies_json)
    assert result is None
    assert Currency.objects.count() == num_of_currencies


@pytest.mark.django_db
def test_bulk_save_exchange_rates_task():
    num_of_rates = random.randint(1, 10)
    exchange_rates = [
        CurrencyExchangeRateEntity(**{
            field.replace('_id', ''): value for field, value in exchange_rate.__dict__.items() \
                if field != 'id' and not field.startswith('_')
        })
        for exchange_rate in CurrencyExchangeRateFactory.build_batch(num_of_rates)
    ]
    exchange_rates_json = json.dumps(
        list(map(dataclasses.asdict, exchange_rates)))
    result = bulk_save_exchange_rates(exchange_rates_json)
    assert result is None
    assert CurrencyExchangeRate.objects.count() == num_of_rates
