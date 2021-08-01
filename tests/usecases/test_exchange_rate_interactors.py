# coding: utf-8

import datetime
import random
from unittest.mock import Mock

import pytest

from src.domain.exchange_rate import CurrencyEntity, CurrencyExchangeRateEntity
from src.usecases.exchange_rate import CurrencyInteractor, CurrencyExchangeRateInteractor
from tests.fixtures import currency, exchange_rate


@pytest.mark.unit
def test_currency_interactor_get(currency):
    currency_repo = Mock()
    currency_repo.get.return_value = currency
    currency_interactor = CurrencyInteractor(currency_repo)
    result = currency_interactor.get(currency.code)
    assert currency_repo.get.called
    assert result.code == currency.code
    assert result.name == currency.name
    assert result.symbol == currency.symbol
    assert CurrencyEntity.to_string(result) == CurrencyEntity.to_string(currency)


@pytest.mark.unit
def test_currency_interactor_get_availables(currency):
    num_of_currencies = random.randint(1, 10)
    currencies_available = [currency for _ in range(num_of_currencies)]
    currency_repo = Mock()
    currency_repo.get_availables.return_value = currencies_available
    currency_interactor = CurrencyInteractor(currency_repo)
    result = currency_interactor.get_availables()
    assert currency_repo.get_availables.called
    assert isinstance(result, list)
    assert len(result) == num_of_currencies
    assert all([isinstance(currency, CurrencyEntity) for currency in result])


@pytest.mark.unit
def test_currency_exchange_rate_interactor_get(exchange_rate):
    exchange_rate_repo = Mock()
    exchange_rate_repo.get.return_value = exchange_rate
    exchange_rate_interactor = CurrencyExchangeRateInteractor(exchange_rate_repo)
    filter = {
        'source_currency': exchange_rate.source_currency,
        'exchanged_currency': exchange_rate.exchanged_currency,
        'valuation_date': exchange_rate.valuation_date
    }
    result = exchange_rate_interactor.get(**filter)
    assert exchange_rate_repo.get.called
    assert result.source_currency == exchange_rate.source_currency
    assert result.exchanged_currency == exchange_rate.exchanged_currency
    assert result.valuation_date == exchange_rate.valuation_date
    assert result.rate_value == exchange_rate.rate_value
    assert CurrencyExchangeRateEntity.to_string(
        result) == CurrencyExchangeRateEntity.to_string(exchange_rate)


@pytest.mark.unit
def test_currency_exchange_rate_interactor_get_latest(exchange_rate):
    exchange_rate_repo = Mock()
    exchange_rate_repo.get.return_value = exchange_rate
    exchange_rate_interactor = CurrencyExchangeRateInteractor(exchange_rate_repo)
    filter = {
        'source_currency': exchange_rate.source_currency,
        'exchanged_currency': exchange_rate.exchanged_currency
    }
    result = exchange_rate_interactor.get_latest(**filter)
    assert exchange_rate_repo.get.called
    assert result.source_currency == exchange_rate.source_currency
    assert result.exchanged_currency == exchange_rate.exchanged_currency
    assert result.valuation_date == datetime.date.today().strftime('%Y-%m-%d')
    assert result.rate_value == exchange_rate.rate_value
    assert CurrencyExchangeRateEntity.to_string(
        result) == CurrencyExchangeRateEntity.to_string(exchange_rate)


@pytest.mark.unit
def test_currency_exchange_rate_interactor_get_rate_series(exchange_rate):
    num_of_rates = random.randint(1, 10)
    rate_series = [round(random.uniform(0.8, 1.2), 6) for _ in range(num_of_rates)]
    exchange_rate_repo = Mock()
    exchange_rate_repo.get_rate_series.return_value = rate_series
    exchange_rate_interactor = CurrencyExchangeRateInteractor(exchange_rate_repo)
    filter = {
        'source_currency': exchange_rate.source_currency,
        'exchanged_currency': exchange_rate.exchanged_currency,
        'date_from': datetime.date.today() + datetime.timedelta(days=-num_of_rates),
        'date_to': datetime.date.today()
    }
    result = exchange_rate_interactor.get_rate_series(**filter)
    assert exchange_rate_repo.get_rate_series.called
    assert isinstance(result, list)
    assert len(result) == num_of_rates
    assert all([isinstance(rate, float) for rate in result])


@pytest.mark.unit
def test_currency_exchange_rate_interactor_get_time_series(exchange_rate):
    series_length = random.randint(1, 10)
    time_series = [exchange_rate for _ in range(series_length)]
    exchange_rate_repo = Mock()
    exchange_rate_repo.get_time_series.return_value = time_series
    exchange_rate_interactor = CurrencyExchangeRateInteractor(exchange_rate_repo)
    filter = {
        'source_currency': exchange_rate.source_currency,
        'exchanged_currency': exchange_rate.exchanged_currency,
        'date_from': datetime.date.today() + datetime.timedelta(days=-series_length),
        'date_to': datetime.date.today()
    }
    result = exchange_rate_interactor.get_time_series(**filter)
    assert exchange_rate_repo.get_time_series.called
    assert isinstance(result, list)
    assert len(result) == series_length
    assert all([isinstance(cer, CurrencyExchangeRateEntity) for cer in result])


@pytest.mark.unit
def test_currency_exchange_rate_interactor_get_all_time_series(exchange_rate):
    series_length = random.randint(1, 10)
    time_series = [exchange_rate for _ in range(series_length)]
    exchange_rate_repo = Mock()
    exchange_rate_repo.get_time_series.return_value = time_series
    exchange_rate_interactor = CurrencyExchangeRateInteractor(exchange_rate_repo)
    filter = {
        'source_currency': exchange_rate.source_currency,
        'date_from': datetime.date.today() + datetime.timedelta(days=-series_length),
        'date_to': datetime.date.today()
    }
    result = exchange_rate_interactor.get_all_time_series(**filter)
    assert exchange_rate_repo.get_time_series.called
    assert isinstance(result, list)
    assert len(result) == series_length
    assert all([isinstance(cer, CurrencyExchangeRateEntity) for cer in result])
