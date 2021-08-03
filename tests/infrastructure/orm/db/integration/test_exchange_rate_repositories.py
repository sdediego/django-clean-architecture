# coding: utf-8

import datetime
import random

import pytest

from src.domain.exchange_rate import CurrencyEntity, CurrencyExchangeRateEntity
from src.infrastructure.orm.db.exchange_rate.repositories import (
    CurrencyDatabaseRepository, CurrencyExchangeRateDatabaseRepository)
from src.interface.repositories.exceptions import EntityDoesNotExist
from tests.fixtures import currency, exchange_rate
from tests.infrastructure.orm.db.integration.factories import (
    CurrencyFactory, CurrencyExchangeRateFactory)


@pytest.mark.django_db
def test_currency_db_repository_get():
    currency = CurrencyFactory.create()
    result = CurrencyDatabaseRepository().get(currency.code)
    assert isinstance(result, CurrencyEntity)
    assert result.code == currency.code
    assert result.name == currency.name
    assert result.symbol == currency.symbol
    assert CurrencyEntity.to_string(result) == str(currency)


@pytest.mark.django_db
def test_currency_db_repository_get_entity_does_not_exist(currency):
    with pytest.raises(EntityDoesNotExist) as err:
        CurrencyDatabaseRepository().get(currency.code)
    assert f'{currency.code} currency code does not exist' in str(err.value)


@pytest.mark.django_db
def test_currency_db_repository_get_availables():
    batch_number = random.randint(1, 10)
    currencies = CurrencyFactory.create_batch(batch_number)
    result = CurrencyDatabaseRepository().get_availables()
    assert isinstance(result, list)
    assert len(currencies) == batch_number
    assert all([isinstance(currency, CurrencyEntity) for currency in result])


@pytest.mark.django_db
def test_exchange_rate_db_repository_get():
    exchange_rate = CurrencyExchangeRateFactory.create()
    result = CurrencyExchangeRateDatabaseRepository().get(
        source_currency=exchange_rate.source_currency,
        exchanged_currency= exchange_rate.exchanged_currency,
        valuation_date=exchange_rate.valuation_date
    )
    assert isinstance(result, CurrencyExchangeRateEntity)
    assert result.source_currency == exchange_rate.source_currency.code
    assert result.exchanged_currency == exchange_rate.exchanged_currency.code
    assert result.valuation_date == exchange_rate.valuation_date.strftime('%Y-%m-%d')
    assert result.rate_value == float(exchange_rate.rate_value)
    assert CurrencyExchangeRateEntity.to_string(result) == str(exchange_rate)


@pytest.mark.django_db
def test_exchange_rate_db_repository_get_entity_does_not_exist(exchange_rate):
    error_message = (
        f'Exchange rate {exchange_rate.source_currency}/{exchange_rate.exchanged_currency} '
        f'for {exchange_rate.valuation_date} does not exist'
    )
    with pytest.raises(EntityDoesNotExist) as err:
        CurrencyExchangeRateDatabaseRepository().get(
            source_currency=exchange_rate.source_currency,
            exchanged_currency= exchange_rate.exchanged_currency,
            valuation_date=exchange_rate.valuation_date
        )
    assert error_message in str(err.value)


@pytest.mark.django_db
def test_exchange_rate_db_repository_get_rate_series():
    batch_number = random.randint(1, 10)
    currencies = CurrencyFactory.create_batch(2)
    CurrencyExchangeRateFactory.create_batch(
        batch_number,
        source_currency=currencies[0],
        exchanged_currency=currencies[1]
    )
    result = CurrencyExchangeRateDatabaseRepository().get_rate_series(
        source_currency=currencies[0],
        exchanged_currency= currencies[1],
        date_from=datetime.date.today() + datetime.timedelta(days=-batch_number),
        date_to=datetime.date.today()
    )
    assert isinstance(result, list)
    assert all([isinstance(rate_value, float) for rate_value in result])


@pytest.mark.django_db
def test_exchange_rate_db_repository_get_time_series():
    batch_number = random.randint(1, 10)
    currencies = CurrencyFactory.create_batch(2)
    CurrencyExchangeRateFactory.create_batch(
        batch_number,
        source_currency=currencies[0],
        exchanged_currency=currencies[1]
    )
    result = CurrencyExchangeRateDatabaseRepository().get_time_series(
        source_currency=currencies[0],
        exchanged_currency= currencies[1],
        date_from=datetime.date.today() + datetime.timedelta(days=-batch_number),
        date_to=datetime.date.today()
    )
    assert isinstance(result, list)
    assert all([isinstance(exchange_rate, CurrencyExchangeRateEntity)
                for exchange_rate in result])
