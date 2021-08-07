# coding: utf-8

import random

from django.core.cache import cache

from src.domain.exchange_rate import CurrencyEntity, CurrencyExchangeRateEntity
from src.infrastructure.orm.cache.exchange_rate.constants import (
    CACHE_AVAILABLE_CURRENCIES_KEY)
from src.infrastructure.orm.cache.exchange_rate.repositories import (
    CurrencyCacheRepository, CurrencyExchangeRateCacheRepository)
from tests.fixtures import currency, exchange_rate


def test_currency_cache_repository_get(currency):
    cache.set(currency.code, currency)
    result = CurrencyCacheRepository().get(currency.code)
    assert isinstance(result, CurrencyEntity)
    assert result.code == currency.code
    assert result.name == currency.name
    assert result.symbol == currency.symbol
    assert CurrencyEntity.to_string(result) == CurrencyEntity.to_string(currency)


def test_currency_cache_repository_get_availables(currency):
    num_of_currencies = random.randint(1, 10)
    currencies = [currency for _ in range(num_of_currencies)]
    cache.set(CACHE_AVAILABLE_CURRENCIES_KEY, currencies)
    result = CurrencyCacheRepository().get_availables()
    assert isinstance(result, list)
    assert len(currencies) == num_of_currencies
    assert all([isinstance(currency, CurrencyEntity) for currency in result])


def test_currency_cache_repository_save(currency):
    CurrencyCacheRepository().save(currency.code, currency)
    result = cache.get(currency.code)
    assert isinstance(result, CurrencyEntity)
    assert result.code == currency.code
    assert result.name == currency.name
    assert result.symbol == currency.symbol
    assert CurrencyEntity.to_string(result) == CurrencyEntity.to_string(currency)


def test_currency_cache_repository_save_availables(currency):
    num_of_currencies = random.randint(1, 10)
    currencies = [currency for _ in range(num_of_currencies)]
    CurrencyCacheRepository().save_availables(currencies)
    result = cache.get(CACHE_AVAILABLE_CURRENCIES_KEY)
    assert isinstance(result, list)
    assert len(currencies) == num_of_currencies
    assert all([isinstance(currency, CurrencyEntity) for currency in result])


def test_currency_exchange_rate_cache_repository_get(exchange_rate):
    source_currency = exchange_rate.source_currency
    exchanged_currency = exchange_rate.exchanged_currency
    valuation_date = exchange_rate.valuation_date
    key = CurrencyExchangeRateCacheRepository.get_exchange_rate_key(
        source_currency, exchanged_currency, valuation_date)
    cache.set(key, exchange_rate)
    result = CurrencyExchangeRateCacheRepository().get(
        source_currency, exchanged_currency, valuation_date)
    assert isinstance(result, CurrencyExchangeRateEntity)
    assert result.source_currency == exchange_rate.source_currency
    assert result.exchanged_currency == exchange_rate.exchanged_currency
    assert result.valuation_date == exchange_rate.valuation_date
    assert result.rate_value == exchange_rate.rate_value
    assert CurrencyExchangeRateEntity.to_string(
        result) == CurrencyExchangeRateEntity.to_string(exchange_rate)


def test_currency_exchange_rate_cache_repository_save(exchange_rate):
    source_currency = exchange_rate.source_currency
    exchanged_currency = exchange_rate.exchanged_currency
    valuation_date = exchange_rate.valuation_date
    key = CurrencyExchangeRateCacheRepository.get_exchange_rate_key(
        source_currency, exchanged_currency, valuation_date)
    CurrencyExchangeRateCacheRepository().save(exchange_rate)
    result = cache.get(key)
    assert isinstance(result, CurrencyExchangeRateEntity)
    assert result.source_currency == exchange_rate.source_currency
    assert result.exchanged_currency == exchange_rate.exchanged_currency
    assert result.valuation_date == exchange_rate.valuation_date
    assert result.rate_value == exchange_rate.rate_value
    assert CurrencyExchangeRateEntity.to_string(
        result) == CurrencyExchangeRateEntity.to_string(exchange_rate)
