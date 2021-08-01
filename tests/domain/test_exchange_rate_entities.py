# coding: utf-8

import datetime
import decimal
import random

import pytest

from src.domain.exchange_rate import (
    CurrencyEntity, CurrencyExchangeRateEntity,
    CurrencyExchangeAmountEntity, TimeWeightedRateEntity)
from tests.fixtures import (
    currency, exchange_rate, exchange_amount, time_weighted_rate)


@pytest.mark.unit
def test_currency_entity_attrs(currency):
    assert isinstance(currency.code, str)
    assert isinstance(currency.name, str)
    assert isinstance(currency.symbol, str)


@pytest.mark.unit
def test_currency_entity_representation(currency):
    entity_str = CurrencyEntity.to_string(currency)
    assert isinstance(entity_str, str)
    assert currency.code in entity_str
    assert currency.name in entity_str
    assert currency.symbol in entity_str


@pytest.mark.unit
def test_currency_exchange_rate_entity_attrs(exchange_rate):
    assert isinstance(exchange_rate.source_currency, str)
    assert isinstance(exchange_rate.exchanged_currency, str)
    assert isinstance(exchange_rate.valuation_date, str)
    assert isinstance(exchange_rate.rate_value, float)


@pytest.mark.unit
def test_currency_exchange_rate_entity_post_init():
    source_currency = 'USD'
    exchanged_currency = 'EUR'
    valuation_date = datetime.date.today()
    rate_value = decimal.Decimal('1.2364380312')
    exchange_rate = CurrencyExchangeRateEntity(
        source_currency=source_currency,
        exchanged_currency=exchanged_currency,
        valuation_date=valuation_date,
        rate_value=rate_value
    )
    assert exchange_rate.source_currency == source_currency
    assert exchange_rate.exchanged_currency == exchanged_currency
    assert exchange_rate.valuation_date == valuation_date.strftime('%Y-%m-%d')
    assert exchange_rate.rate_value == round(float(rate_value), 6)


@pytest.mark.unit
def test_currency_exchange_rate_entity_representation(exchange_rate):
    entity_str = CurrencyExchangeRateEntity.to_string(exchange_rate)
    assert isinstance(entity_str, str)
    assert exchange_rate.source_currency in entity_str
    assert exchange_rate.exchanged_currency in entity_str
    assert exchange_rate.valuation_date in entity_str
    assert str(exchange_rate.rate_value) in entity_str


@pytest.mark.unit
def test_currency_exchange_rate_entity_calculate_amount(exchange_rate):
    amount = round(random.uniform(10, 50), 2)
    result = exchange_rate.calculate_amount(amount)
    assert result == round(amount * exchange_rate.rate_value, 2)


@pytest.mark.unit
def test_currency_exchange_amount_entity_attrs(exchange_amount):
    assert isinstance(exchange_amount.exchanged_currency, str)
    assert isinstance(exchange_amount.exchanged_amount, float)
    assert isinstance(exchange_amount.rate_value, float)


@pytest.mark.unit
def test_currency_exchange_amount_entity_post_init(currency):
    exchanged_currency = currency
    exchanged_amount = decimal.Decimal('17.3423')
    rate_value = decimal.Decimal('1.2364380312')
    exchange_amount = CurrencyExchangeAmountEntity(
        exchanged_currency=exchanged_currency,
        exchanged_amount=exchanged_amount,
        rate_value=rate_value
    )
    assert exchange_amount.exchanged_currency == currency.code
    assert exchange_amount.exchanged_amount == round(float(exchanged_amount), 2)
    assert exchange_amount.rate_value == round(float(rate_value), 6)


@pytest.mark.unit
def test_currency_exchange_amount_entity_representation(exchange_amount):
    entity_str = CurrencyExchangeAmountEntity.to_string(exchange_amount)
    assert isinstance(entity_str, str)
    assert exchange_amount.exchanged_currency in entity_str
    assert str(exchange_amount.exchanged_amount) in entity_str
    assert str(exchange_amount.rate_value) in entity_str


@pytest.mark.unit
def test_time_weighted_rate_entity_attrs(time_weighted_rate):
    assert isinstance(time_weighted_rate.time_weighted_rate, float)


@pytest.mark.unit
def test_time_weighted_rate_entity_representation(time_weighted_rate):
    entity_str = TimeWeightedRateEntity.to_string(time_weighted_rate)
    assert isinstance(entity_str, str)
    assert str(time_weighted_rate.time_weighted_rate) in entity_str
