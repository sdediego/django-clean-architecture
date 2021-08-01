# coding: utf-8

import datetime
import random
from http import HTTPStatus
from unittest.mock import Mock

import pytest

from src.interface.controllers.exchange_rate import (
    CurrencyController, CurrencyExchangeRateController)
from src.interface.repositories.exceptions import EntityDoesNotExist
from tests.fixtures import currency, exchange_rate


@pytest.mark.unit
def test_currency_controller_get(currency):
    currency_interator = Mock()
    currency_interator.get.return_value = currency
    controller = CurrencyController(currency_interator)
    data, status = controller.get(currency.code)
    assert currency_interator.get.called
    assert status == HTTPStatus.OK.value
    assert data['code'] == currency.code
    assert data['name'] == currency.name
    assert data['symbol'] == currency.symbol


@pytest.mark.unit
def test_currency_controller_get_entity_does_not_exist(currency):
    error_message = f'{currency.code} currency code does not exist'
    currency_interator = Mock()
    currency_interator.get.side_effect = EntityDoesNotExist(error_message)
    controller = CurrencyController(currency_interator)
    data, status = controller.get(currency.code)
    assert currency_interator.get.called
    assert status == HTTPStatus.NOT_FOUND.value
    assert 'error' in data
    assert data['error'] == error_message


@pytest.mark.unit
def test_currency_controller_list(currency):
    num_of_currencies = random.randint(1, 5)
    currency_interator = Mock()
    currency_interator.get_availables.return_value = [
        currency for _ in range(num_of_currencies)]
    controller = CurrencyController(currency_interator)
    data, status = controller.list()
    assert currency_interator.get_availables.called
    assert status == HTTPStatus.OK.value
    assert isinstance(data, list)
    assert all([key in currency.keys() for key in [
                'code', 'name', 'symbol'] for currency in data])


@pytest.mark.unit
def test_exchange_rate_controller_convert(exchange_rate):
    amount = round(random.uniform(1, 100), 2)
    params = {
        'source_currency': exchange_rate.source_currency,
        'exchanged_currency': exchange_rate.exchanged_currency,
        'amount': amount
    }
    exchange_rate_interactor = Mock()
    exchange_rate_interactor.get_latest.return_value = exchange_rate
    controller = CurrencyExchangeRateController(exchange_rate_interactor)
    data, status = controller.convert(params)
    assert exchange_rate_interactor.get_latest.called
    assert status == HTTPStatus.OK.value
    assert data['exchanged_currency'] == params['exchanged_currency']
    assert data['exchanged_amount'] == exchange_rate.calculate_amount(amount)
    assert data['rate_value'] == exchange_rate.rate_value


@pytest.mark.unit
def test_exchange_rate_controller_convert_errors(exchange_rate):
    params = {
        'source_currency': exchange_rate,
        'exchanged_currency': exchange_rate,
        'amount': 'amount'
    }
    exchange_rate_interactor = Mock()
    exchange_rate_interactor.get_latest.return_value = exchange_rate
    controller = CurrencyExchangeRateController(exchange_rate_interactor)
    data, status = controller.convert(params)
    assert not exchange_rate_interactor.get_latest.called
    assert status == HTTPStatus.BAD_REQUEST.value
    assert isinstance(data, dict)
    assert 'errors' in data
    assert all([key in data['errors'].keys() for key in params.keys()])


@pytest.mark.unit
def test_exchange_rate_controller_convert_entity_does_not_exist(exchange_rate):
    params = {
        'source_currency': exchange_rate.source_currency,
        'exchanged_currency': exchange_rate.exchanged_currency,
        'amount': round(random.uniform(1, 100), 2)
    }
    error_message = (
        f'Exchange rate {exchange_rate.source_currency}/{exchange_rate.exchanged_currency} '
        f'for {exchange_rate.valuation_date} does not exist'
    )
    error = EntityDoesNotExist(error_message)
    exchange_rate_interactor = Mock()
    exchange_rate_interactor.get_latest.side_effect = error
    controller = CurrencyExchangeRateController(exchange_rate_interactor)
    data, status = controller.convert(params)
    assert exchange_rate_interactor.get_latest.called
    assert status == HTTPStatus.NOT_FOUND.value
    assert 'error' in data
    assert data['error'] == error_message


@pytest.mark.unit
def test_exchange_rate_controller_list(exchange_rate):
    series_length = random.randint(1, 10)
    params = {
        'source_currency': exchange_rate.source_currency,
        'date_from': (
            datetime.date.today() + datetime.timedelta(days=-series_length)).strftime('%Y-%m-%d'),
        'date_to': datetime.date.today().strftime('%Y-%m-%d')
    }
    exchange_rate_interactor = Mock()
    exchange_rate_interactor.get_all_time_series.return_value = [
        exchange_rate for _ in range(series_length)]
    controller = CurrencyExchangeRateController(exchange_rate_interactor)
    data, status = controller.list(params)
    assert exchange_rate_interactor.get_all_time_series.called
    assert status == HTTPStatus.OK.value
    assert isinstance(data, list)
    assert all([key in exchange_rate.keys() for key in [
               'exchanged_currency', 'valuation_date', 'rate_value'] for exchange_rate in data])


@pytest.mark.unit
def test_exchange_rate_controller_list_errors(exchange_rate):
    series_length = random.randint(1, 10)
    params = {
        'source_currency': exchange_rate,
        'date_from': datetime.date.today() + datetime.timedelta(days=-series_length),
        'date_to': datetime.date.today()
    }
    exchange_rate_interactor = Mock()
    exchange_rate_interactor.get_all_time_series.return_value = [
        exchange_rate for _ in range(series_length)]
    controller = CurrencyExchangeRateController(exchange_rate_interactor)
    data, status = controller.list(params)
    assert not exchange_rate_interactor.get_all_time_series.called
    assert status == HTTPStatus.BAD_REQUEST.value
    assert isinstance(data, dict)
    assert 'errors' in data
    assert all([key in data['errors'].keys() for key in params.keys()])


@pytest.mark.unit
def test_exchange_rate_controller_calculate_twr(exchange_rate):
    num_of_rates = random.randint(1, 10)
    params = {
        'source_currency': exchange_rate.source_currency,
        'exchanged_currency': exchange_rate.exchanged_currency,
        'date_from': (
            datetime.date.today() + datetime.timedelta(days=-num_of_rates)).strftime('%Y-%m-%d'),
        'date_to': datetime.date.today().strftime('%Y-%m-%d')
    }
    exchange_rate_interactor = Mock()
    exchange_rate_interactor.get_rate_series.return_value = [
        round(random.uniform(0.8, 1.2), 6) for _ in range(num_of_rates)]
    controller = CurrencyExchangeRateController(exchange_rate_interactor)
    data, status = controller.calculate_twr(params)
    assert exchange_rate_interactor.get_rate_series.called
    assert status == HTTPStatus.OK.value
    assert isinstance(data, dict)
    assert isinstance(data.get('time_weighted_rate'), float)


@pytest.mark.unit
def test_exchange_rate_controller_calculate_twr_errors(currency):
    num_of_rates = random.randint(1, 10)
    params = {
        'source_currency': currency,
        'exchanged_currency': currency,
        'date_from': datetime.date.today() + datetime.timedelta(days=-num_of_rates),
        'date_to': datetime.date.today()
    }
    exchange_rate_interactor = Mock()
    exchange_rate_interactor.get_rate_series.return_value = [
        round(random.uniform(0.8, 1.2), 6) for _ in range(num_of_rates)]
    controller = CurrencyExchangeRateController(exchange_rate_interactor)
    data, status = controller.calculate_twr(params)
    assert not exchange_rate_interactor.get_rate_series.called
    assert status == HTTPStatus.BAD_REQUEST.value
    assert isinstance(data, dict)
    assert 'errors' in data
    assert all([key in data['errors'].keys() for key in params.keys()])
