# coding: utf-8

import datetime
import random
from unittest.mock import Mock

import pytest

from src.domain.exchange_rate import CurrencyEntity, CurrencyExchangeRateEntity
from src.interface.repositories.exchange_rate import (
    CurrencyRepository, CurrencyExchangeRateRepository)
from tests.fixtures import currency, exchange_rate


@pytest.mark.unit
def test_currency_repository_database_get(currency):
    db_repo = Mock()
    db_repo.get.return_value = currency
    cache_repo = Mock()
    cache_repo.get.return_value = None
    cache_repo.save.return_value = None
    currency_repo = CurrencyRepository(db_repo, cache_repo)
    result = currency_repo.get(currency.code)
    assert cache_repo.get.called
    assert cache_repo.save.called
    assert db_repo.get.called
    assert result.code == currency.code
    assert result.name == currency.name
    assert result.symbol == currency.symbol
    assert CurrencyEntity.to_string(
        result) == CurrencyEntity.to_string(currency)


@pytest.mark.unit
def test_currency_repository_cache_get(currency):
    db_repo = Mock()
    db_repo.get.return_value = None
    cache_repo = Mock()
    cache_repo.get.return_value = currency
    cache_repo.save.return_value = None
    currency_repo = CurrencyRepository(db_repo, cache_repo)
    result = currency_repo.get(currency.code)
    assert cache_repo.get.called
    assert not cache_repo.save.called
    assert not db_repo.get.called
    assert result.code == currency.code
    assert result.name == currency.name
    assert result.symbol == currency.symbol
    assert CurrencyEntity.to_string(
        result) == CurrencyEntity.to_string(currency)


@pytest.mark.unit
def test_currency_repository_database_get_availables(currency):
    num_of_currencies = random.randint(1, 10)
    currencies_available = [currency for _ in range(num_of_currencies)]
    db_repo = Mock()
    db_repo.get_availables.return_value = currencies_available
    cache_repo = Mock()
    cache_repo.get_availables.return_value = None
    cache_repo.save_availables.return_value = None
    currency_repo = CurrencyRepository(db_repo, cache_repo)
    result = currency_repo.get_availables()
    assert db_repo.get_availables.called
    assert cache_repo.get_availables.called
    assert cache_repo.save_availables.called
    assert isinstance(result, list)
    assert len(result) == num_of_currencies
    assert all([isinstance(currency, CurrencyEntity) for currency in result])


@pytest.mark.unit
def test_currency_repository_cache_get_availables(currency):
    num_of_currencies = random.randint(1, 10)
    currencies_available = [currency for _ in range(num_of_currencies)]
    db_repo = Mock()
    db_repo.get_availables.return_value = None
    cache_repo = Mock()
    cache_repo.get_availables.return_value = currencies_available
    cache_repo.save_availables.return_value = None
    currency_repo = CurrencyRepository(db_repo, cache_repo)
    result = currency_repo.get_availables()
    assert cache_repo.get_availables.called
    assert not cache_repo.save_availables.called
    assert not db_repo.get_availables.called
    assert isinstance(result, list)
    assert len(result) == num_of_currencies
    assert all([isinstance(currency, CurrencyEntity) for currency in result])


@pytest.mark.unit
def test_currency_exchange_rate_repository_get(exchange_rate):
    db_repo = Mock()
    db_repo.get.return_value = exchange_rate
    exchange_rate_repo = CurrencyExchangeRateRepository(db_repo)
    filter = {
        'source_currency': exchange_rate.source_currency,
        'exchanged_currency': exchange_rate.exchanged_currency,
        'valuation_date': exchange_rate.valuation_date
    }
    result = exchange_rate_repo.get(**filter)
    assert db_repo.get.called
    assert result.source_currency == exchange_rate.source_currency
    assert result.exchanged_currency == exchange_rate.exchanged_currency
    assert result.valuation_date == exchange_rate.valuation_date
    assert result.rate_value == exchange_rate.rate_value
    assert CurrencyExchangeRateEntity.to_string(
        result) == CurrencyExchangeRateEntity.to_string(exchange_rate)


@pytest.mark.unit
def test_currency_exchange_rate_repository_get_rate_series(exchange_rate):
    num_of_rates = random.randint(1, 10)
    rate_series = [round(random.uniform(0.8, 1.2), 6) for _ in range(num_of_rates)]
    db_repo = Mock()
    db_repo.get_rate_series.return_value = rate_series
    exchange_rate_repo = CurrencyExchangeRateRepository(db_repo)
    filter = {
        'source_currency': exchange_rate.source_currency,
        'exchanged_currency': exchange_rate.exchanged_currency,
        'date_from': datetime.date.today() + datetime.timedelta(days=-num_of_rates),
        'date_to': datetime.date.today()
    }
    result = exchange_rate_repo.get_rate_series(**filter)
    assert db_repo.get_rate_series.called
    assert isinstance(result, list)
    assert len(result) == num_of_rates
    assert all([isinstance(rate, float) for rate in result])


@pytest.mark.unit
def test_currency_exchange_rate_repository_get_time_series(exchange_rate):
    series_length = random.randint(1, 10)
    time_series = [exchange_rate for _ in range(series_length)]
    db_repo = Mock()
    db_repo.get_time_series.return_value = time_series
    exchange_rate_repo = CurrencyExchangeRateRepository(db_repo)
    filter = {
        'source_currency': exchange_rate.source_currency,
        'exchanged_currency': exchange_rate.exchanged_currency,
        'date_from': datetime.date.today() + datetime.timedelta(days=-series_length),
        'date_to': datetime.date.today()
    }
    result = exchange_rate_repo.get_time_series(**filter)
    assert db_repo.get_time_series.called
    assert isinstance(result, list)
    assert len(result) == series_length
    assert all([isinstance(cer, CurrencyExchangeRateEntity) for cer in result])
