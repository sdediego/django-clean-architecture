# coding: utf-8

import dataclasses
import json
import random
from unittest.mock import patch

import pytest

from src.infrastructure.orm.db.exchange_rate.models import (
    Currency, CurrencyExchangeRate)
from src.infrastructure.orm.db.exchange_rate.tasks import (
    bulk_save_currencies, bulk_save_exchange_rates, save_currency, save_exchange_rate)
from tests.fixtures import currency, exchange_rate
from tests.infrastructure.orm.db.factories.exchange_rate import CurrencyFactory


@pytest.mark.unit
@patch.object(Currency, 'objects')
def test_save_currency_task(mock_objects, currency):
    mock_create = mock_objects.create
    mock_create.return_value = None
    currency_json = json.dumps(dataclasses.asdict(currency))
    result = save_currency(currency_json)
    assert result is None
    assert mock_create.called


@pytest.mark.unit
@patch.object(CurrencyExchangeRate, 'objects')
@patch('src.infrastructure.orm.db.exchange_rate.tasks.get_currency')
def test_save_exchange_rate_task(mock_get_currency, mock_objects, exchange_rate):
    mock_create = mock_objects.create
    mock_create.return_value = None
    mock_get_currency.return_value = CurrencyFactory.build()
    exchange_rate_json = json.dumps(dataclasses.asdict(exchange_rate))
    result = save_exchange_rate(exchange_rate_json)
    assert result is None
    assert mock_create.called


@pytest.mark.unit
@patch.object(Currency, 'objects')
def test_bulk_save_currencies_task(mock_objects, currency):
    mock_bulk_create = mock_objects.bulk_create
    mock_bulk_create.return_value = None
    currencies = [currency for _ in range(random.randint(1, 10))]
    currencies_json = json.dumps(list(map(dataclasses.asdict, currencies)))
    result = bulk_save_currencies(currencies_json)
    assert result is None
    assert mock_bulk_create.called


@pytest.mark.unit
@patch.object(CurrencyExchangeRate, 'objects')
@patch('src.infrastructure.orm.db.exchange_rate.tasks.get_currency')
def test_bulk_save_exchange_rates_task(mock_get_currency, mock_objects, exchange_rate):
    mock_bulk_create = mock_objects.bulk_create
    mock_bulk_create.return_value = None
    mock_get_currency.return_value = CurrencyFactory.build()
    exchange_rates = [exchange_rate for _ in range(random.randint(1, 10))]
    exchange_rate_json = json.dumps(list(map(dataclasses.asdict, exchange_rates)))
    result = bulk_save_exchange_rates(exchange_rate_json)
    assert result is None
    assert mock_bulk_create.called
