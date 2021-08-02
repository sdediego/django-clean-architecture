# coding: utf-8

import datetime
import random
from unittest.mock import Mock, patch

import pytest

from src.domain.exchange_rate import CurrencyEntity, CurrencyExchangeRateEntity
from src.infrastructure.orm.db.exchange_rate.models import (
    Currency, CurrencyExchangeRate)
from src.infrastructure.orm.db.exchange_rate.repositories import (
    CurrencyDatabaseRepository, CurrencyExchangeRateDatabaseRepository)
from src.interface.repositories.exceptions import EntityDoesNotExist
from tests.fixtures import currency, exchange_rate


@pytest.mark.unit
@patch.object(Currency, 'objects')
def test_currency_db_repository_get(mock_objets, currency):
    mock_filter = mock_objets.filter
    mock_filter.return_value = Mock()
    mock_values = mock_filter.return_value.values
    mock_values.return_value = Mock()
    mock_first = mock_values.return_value.first
    mock_first.return_value = vars(currency)
    result = CurrencyDatabaseRepository().get(currency.code)
    assert isinstance(result, CurrencyEntity)
    assert result.code == currency.code
    assert result.name == currency.name
    assert result.symbol == currency.symbol
    assert CurrencyEntity.to_string(result) == CurrencyEntity.to_string(currency)


@pytest.mark.unit
@patch.object(Currency, 'objects')
def test_currency_db_repository_get_entity_does_not_exist(mock_objets, currency):
    mock_filter = mock_objets.filter
    mock_filter.return_value = Mock()
    mock_values = mock_filter.return_value.values
    mock_values.return_value = Mock()
    mock_first = mock_values.return_value.first
    mock_first.return_value = None
    with pytest.raises(EntityDoesNotExist) as err:
        CurrencyDatabaseRepository().get(currency.code)
    assert f'{currency.code} currency code does not exist' in str(err.value)


@pytest.mark.unit
@patch.object(Currency, 'objects')
def test_currency_db_repository_get_availables(mock_objets, currency):
    num_of_currencies = random.randint(1, 10)
    mock_values = mock_objets.values
    mock_values.return_value = [vars(currency) for _ in range(num_of_currencies)]
    result = CurrencyDatabaseRepository().get_availables()
    assert isinstance(result, list)
    assert all([isinstance(currency, CurrencyEntity) for currency in result])


@pytest.mark.unit
@patch.object(CurrencyExchangeRate, 'objects')
def test_exchange_rate_db_repository_get(mock_objets, exchange_rate):
    mock_filter = mock_objets.filter
    mock_filter.return_value = Mock()
    mock_values = mock_filter.return_value.values
    mock_values.return_value = Mock()
    mock_first = mock_values.return_value.first
    mock_first.return_value = vars(exchange_rate)
    result = CurrencyExchangeRateDatabaseRepository().get(
        source_currency=exchange_rate.source_currency,
        exchanged_currency= exchange_rate.exchanged_currency,
        valuation_date=exchange_rate.valuation_date
    )
    assert isinstance(result, CurrencyExchangeRateEntity)
    assert result.source_currency == exchange_rate.source_currency
    assert result.exchanged_currency == exchange_rate.exchanged_currency
    assert result.valuation_date == exchange_rate.valuation_date
    assert result.rate_value == exchange_rate.rate_value
    assert CurrencyExchangeRateEntity.to_string(
        result) == CurrencyExchangeRateEntity.to_string(exchange_rate)


@pytest.mark.unit
@patch.object(CurrencyExchangeRate, 'objects')
def test_exchange_rate_db_repository_get_entity_does_not_exist(mock_objets, exchange_rate):
    mock_filter = mock_objets.filter
    mock_filter.return_value = Mock()
    mock_values = mock_filter.return_value.values
    mock_values.return_value = Mock()
    mock_first = mock_values.return_value.first
    mock_first.return_value = None
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


@pytest.mark.unit
@patch.object(CurrencyExchangeRate, 'objects')
def test_exchange_rate_db_repository_get_rate_series(mock_objets, exchange_rate):
    num_of_rates = random.randint(1, 10)
    mock_filter = mock_objets.filter
    mock_filter.return_value = Mock()
    mock_values_list = mock_filter.return_value.values_list
    mock_values_list.return_value = [
        round(random.uniform(0.5, 1.5), 6) for _ in range(num_of_rates)]
    result = CurrencyExchangeRateDatabaseRepository().get_rate_series(
        source_currency=exchange_rate.source_currency,
        exchanged_currency= exchange_rate.exchanged_currency,
        date_from=datetime.date.today() + datetime.timedelta(days=-num_of_rates),
        date_to=datetime.date.today()
    )
    assert isinstance(result, list)
    assert all([isinstance(rate_value, float) for rate_value in result])


@pytest.mark.unit
@patch.object(CurrencyExchangeRate, 'objects')
def test_exchange_rate_db_repository_get_time_series(mock_objets, exchange_rate):
    num_of_rates = random.randint(1, 10)
    mock_filter = mock_objets.filter
    mock_filter.return_value = Mock()
    mock_values = mock_filter.return_value.values
    mock_values.return_value = [vars(exchange_rate) for _ in range(num_of_rates)]
    result = CurrencyExchangeRateDatabaseRepository().get_time_series(
        source_currency=exchange_rate.source_currency,
        exchanged_currency= exchange_rate.exchanged_currency,
        date_from=datetime.date.today() + datetime.timedelta(days=-num_of_rates),
        date_to=datetime.date.today()
    )
    assert isinstance(result, list)
    assert all([isinstance(exchange_rate, CurrencyExchangeRateEntity)
                for exchange_rate in result])
