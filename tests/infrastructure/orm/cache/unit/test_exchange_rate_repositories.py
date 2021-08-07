# coding: utf-8

import random
from unittest.mock import patch

from django.core.cache import cache

import pytest

from src.domain.exchange_rate import CurrencyEntity, CurrencyExchangeRateEntity
from src.infrastructure.orm.cache.exchange_rate.repositories import (
    CurrencyCacheRepository, CurrencyExchangeRateCacheRepository)
from tests.fixtures import currency, exchange_rate


@pytest.mark.unit
@patch.object(cache, 'get')
def test_currency_cache_repository_get(mock_get, currency):
    mock_get.return_value = currency
    result = CurrencyCacheRepository().get(currency.code)
    assert mock_get.called
    assert isinstance(result, CurrencyEntity)
    assert result.code == currency.code
    assert result.name == currency.name
    assert result.symbol == currency.symbol
    assert CurrencyEntity.to_string(result) == CurrencyEntity.to_string(currency)


@pytest.mark.unit
@patch.object(cache, 'get')
def test_currency_cache_repository_get_availables(mock_get, currency):
    num_of_currencies = random.randint(1, 10)
    mock_get.return_value = [currency for _ in range(num_of_currencies)]
    result = CurrencyCacheRepository().get_availables()
    assert mock_get.called
    assert isinstance(result, list)
    assert all([isinstance(currency, CurrencyEntity) for currency in result])


@pytest.mark.unit
@patch.object(cache, 'set')
def test_currency_cache_repository_save(mock_set, currency):
    mock_set.return_value = None
    result = CurrencyCacheRepository().save(currency.code, currency)
    assert mock_set.called
    assert result is None


@pytest.mark.unit
@patch.object(cache, 'set')
def test_currency_cache_repository_save_availables(mock_set, currency):
    mock_set.return_value = None
    num_of_currencies = random.randint(1, 10)
    currencies = [currency for _ in range(num_of_currencies)]
    result = CurrencyCacheRepository().save_availables(currencies)
    assert mock_set.called
    assert result is None


@pytest.mark.unit
@patch.object(cache, 'get')
def test_currency_exchange_rate_cache_repository_get(mock_get, exchange_rate):
    mock_get.return_value = exchange_rate
    result = CurrencyExchangeRateCacheRepository().get(
        exchange_rate.source_currency,
        exchange_rate.exchanged_currency,
        exchange_rate.valuation_date
    )
    assert mock_get.called
    assert isinstance(result, CurrencyExchangeRateEntity)
    assert result.source_currency == exchange_rate.source_currency
    assert result.exchanged_currency == exchange_rate.exchanged_currency
    assert result.valuation_date == exchange_rate.valuation_date
    assert result.rate_value == exchange_rate.rate_value
    assert CurrencyExchangeRateEntity.to_string(
        result) == CurrencyExchangeRateEntity.to_string(exchange_rate)


@pytest.mark.unit
@patch.object(cache, 'set')
def test_currency_exchange_rate_cache_repository_save(mock_set, exchange_rate):
    mock_set.return_value = None
    result = CurrencyExchangeRateCacheRepository().save(exchange_rate)
    assert mock_set.called
    assert result is None
