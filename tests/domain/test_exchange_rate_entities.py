# coding: utf-8

import datetime
import decimal
import random

import pytest

from src.domain.exchange_rate import CurrencyEntity, CurrencyExchangeRateEntity
from tests.fixtures import currency, currency_exchange_rate


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
def test_currency_exchange_rate_entity_attrs(currency_exchange_rate):
    assert isinstance(currency_exchange_rate.source_currency, str)
    assert isinstance(currency_exchange_rate.exchanged_currency, str)
    assert isinstance(currency_exchange_rate.valuation_date, str)
    assert isinstance(currency_exchange_rate.rate_value, float)


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
def test_currency_exchange_rate_entity_representation(currency_exchange_rate):
    entity_str = CurrencyExchangeRateEntity.to_string(currency_exchange_rate)
    assert isinstance(entity_str, str)
    assert currency_exchange_rate.source_currency in entity_str
    assert currency_exchange_rate.exchanged_currency in entity_str
    assert currency_exchange_rate.valuation_date in entity_str
    assert str(currency_exchange_rate.rate_value) in entity_str


@pytest.mark.unit
def test_currency_exchange_rate_entity_calculate_amount(currency_exchange_rate):
    amount = round(random.uniform(10, 50), 2)
    result = currency_exchange_rate.calculate_amount(amount)
    assert result == round(amount * currency_exchange_rate.rate_value, 2)
