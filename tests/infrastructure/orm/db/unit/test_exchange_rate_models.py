# coding: utf-8

import pytest

from src.domain.exchange_rate import CurrencyEntity, CurrencyExchangeRateEntity
from src.infrastructure.orm.db.exchange_rate.models import (
    Currency, CurrencyExchangeRate)
from tests.fixtures import currency, exchange_rate


def create_currency_model(currency):
    return Currency(
        code=currency.code,
        name=currency.name,
        symbol=currency.symbol
    )


def create_exchange_rate_model(currency, exchange_rate):
    return CurrencyExchangeRate(
        source_currency=create_currency_model(currency),
        exchanged_currency=create_currency_model(currency),
        valuation_date=exchange_rate.valuation_date,
        rate_value=exchange_rate.rate_value
    )


@pytest.mark.unit
def test_currency_attrs(currency):
    model = create_currency_model(currency)
    assert isinstance(model, Currency)
    assert isinstance(model.code, str)
    assert isinstance(model.name, str)
    assert isinstance(model.symbol, str)


@pytest.mark.unit
def test_currency_representation(currency):
    model = create_currency_model(currency)
    assert str(model) == CurrencyEntity.to_string(currency)


@pytest.mark.unit
def test_currency_exchange_rate_attrs(currency, exchange_rate):
    model = create_exchange_rate_model(currency, exchange_rate)
    assert isinstance(model, CurrencyExchangeRate)
    assert isinstance(model.source_currency, Currency)
    assert isinstance(model.exchanged_currency, Currency)
    assert isinstance(model.valuation_date, str)
    assert isinstance(model.rate_value, float)


@pytest.mark.unit
def test_currency_exchange_rate_entity_representation(currency, exchange_rate):
    model = create_exchange_rate_model(currency, exchange_rate)
    entity_str = CurrencyExchangeRateEntity.to_string(exchange_rate)
    assert model.source_currency.code in entity_str
    assert model.valuation_date in entity_str
    assert str(model.rate_value) in entity_str
