# coding: utf-8

import datetime
import random

import pytest

from src.domain.exchange_rate import (
    CurrencyExchangeAmountEntity, TimeWeightedRateEntity)
from src.interface.serializers.exchange_rate import (
    CurrencySerializer, CurrencyExchangeRateConvertSerializer,
    CurrencyExchangeRateAmountSerializer, CurrencyExchangeRateListSerializer,
    CurrencyExchangeRateSerializer, TimeWeightedRateListSerializer,
    TimeWeightedRateSerializer)
from tests.fixtures import currency, exchange_rate


@pytest.mark.unit
def test_currency_serializer(currency):
    valid_data = CurrencySerializer().dump(currency)
    assert valid_data['code'] == currency.code
    assert valid_data['name'] == currency.name
    assert valid_data['symbol'] == currency.symbol


@pytest.mark.unit
def test_currency_exchange_rate_convert_serializer(exchange_rate):
    data = {
        'source_currency': exchange_rate.source_currency,
        'exchanged_currency': exchange_rate.exchanged_currency,
        'amount': round(random.uniform(1, 100), 2)
    }
    valid_data = CurrencyExchangeRateConvertSerializer().load(data)
    assert valid_data['source_currency'] == data['source_currency']
    assert valid_data['exchanged_currency'] == data['exchanged_currency']
    assert valid_data['amount'] == data['amount']


@pytest.mark.unit
def test_currency_exchange_rate_convert_serializer_validation_error(exchange_rate):
    data = {
        'source_currency': exchange_rate,
        'exchanged_currency': exchange_rate,
        'amount': 'amount'
    }
    invalid_data = CurrencyExchangeRateConvertSerializer().load(data)
    assert 'errors' in invalid_data
    assert all([key in invalid_data['errors'].keys() for key in data.keys()])


@pytest.mark.unit
def test_currency_exchange_rate_amount_serializer(exchange_rate):
    data = CurrencyExchangeAmountEntity(
        exchanged_currency=exchange_rate.exchanged_currency,
        exchanged_amount=round(random.uniform(1, 100), 2),
        rate_value=exchange_rate.rate_value
    )
    valid_data = CurrencyExchangeRateAmountSerializer().dump(data)
    assert valid_data['exchanged_currency'] == data.exchanged_currency
    assert valid_data['exchanged_amount'] == data.exchanged_amount
    assert valid_data['rate_value'] == data.rate_value


@pytest.mark.unit
def test_currency_exchange_rate_list_serializer(exchange_rate):
    data = {
        'source_currency': exchange_rate.source_currency,
        'date_from': (
            datetime.date.today() + datetime.timedelta(days=-5)
        ).strftime('%Y-%m-%d'),
        'date_to': datetime.date.today().strftime('%Y-%m-%d')
    }
    valid_data = CurrencyExchangeRateListSerializer().load(data)
    assert valid_data['source_currency'] == data['source_currency']
    assert valid_data['date_from'] == data['date_from']
    assert valid_data['date_to'] == data['date_to'] 


@pytest.mark.unit
def test_currency_exchange_rate_list_serializer_validation_error(exchange_rate):
    data = {
        'source_currency': exchange_rate,
        'date_from': datetime.date.today(),
        'date_to': datetime.date.today()
    }
    invalid_data = CurrencyExchangeRateListSerializer().load(data)
    assert 'errors' in invalid_data
    assert all([key in invalid_data['errors'].keys() for key in data.keys()])


@pytest.mark.unit
def test_currency_exchange_rate_serializer(exchange_rate):
    data = exchange_rate
    valid_data = CurrencyExchangeRateSerializer().dump(data)
    assert valid_data['exchanged_currency'] == data.exchanged_currency
    assert valid_data['valuation_date'] == data.valuation_date
    assert valid_data['rate_value'] == data.rate_value


@pytest.mark.unit
def test_time_weighted_rate_list_serializer(exchange_rate):
    data = {
        'source_currency': exchange_rate.source_currency,
        'exchanged_currency': exchange_rate.exchanged_currency,
        'date_from': (
            datetime.date.today() + datetime.timedelta(days=-5)
        ).strftime('%Y-%m-%d'),
        'date_to': datetime.date.today().strftime('%Y-%m-%d')
    }
    valid_data = TimeWeightedRateListSerializer().load(data)
    assert valid_data['source_currency'] == data['source_currency']
    assert valid_data['exchanged_currency'] == data['exchanged_currency']
    assert valid_data['date_from'] == data['date_from']
    assert valid_data['date_to'] == data['date_to'] 


@pytest.mark.unit
def test_time_weighted_rate_list_serializer_validation_error(exchange_rate):
    data = {
        'source_currency': exchange_rate,
        'exchanged_currence': exchange_rate,
        'date_from': datetime.date.today(),
        'date_to': datetime.date.today()
    }
    invalid_data = TimeWeightedRateListSerializer().load(data)
    assert 'errors' in invalid_data
    assert all([key in invalid_data['errors'].keys() for key in data.keys()])


@pytest.mark.unit
def test_time_weighted_rate_serializer():
    data = TimeWeightedRateEntity(
        time_weighted_rate=random.uniform(0.5, 1.5)
    )
    valid_data = TimeWeightedRateSerializer().dump(data)
    assert valid_data['time_weighted_rate'] == data.time_weighted_rate
