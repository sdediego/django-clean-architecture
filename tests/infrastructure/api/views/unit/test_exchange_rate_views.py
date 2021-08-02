# coding: utf-8

import datetime
import random
from http import HTTPStatus
from unittest.mock import Mock

from django.test.client import RequestFactory

import pytest

from src.infrastructure.api.views.exchange_rate import (
    CurrencyViewSet, CurrencyExchangeRateViewSet)
from tests.fixtures import currency, exchange_rate


@pytest.mark.unit
def test_currency_viewset_get(currency):
    viewset = CurrencyViewSet()
    viewset.viewset_factory = Mock()
    viewset.viewset_factory.create.return_value = Mock()
    viewset.viewset_factory.create.return_value.get.return_value = (
        vars(currency),
        HTTPStatus.OK.value
    )
    response = viewset.get(RequestFactory(), currency.code)
    assert hasattr(response, 'status_code')
    assert response.status_code == HTTPStatus.OK.value
    assert hasattr(response, 'data')
    assert isinstance(response.data, dict)


@pytest.mark.unit
def test_currency_viewset_list(currency):
    viewset = CurrencyViewSet()
    viewset.viewset_factory = Mock()
    viewset.viewset_factory.create.return_value = Mock()
    viewset.viewset_factory.create.return_value.list.return_value = (
        [vars(currency) for _ in range(random.randint(1, 10))],
        HTTPStatus.OK.value
    )
    response = viewset.list(RequestFactory(), currency.code)
    assert hasattr(response, 'status_code')
    assert response.status_code == HTTPStatus.OK.value
    assert hasattr(response, 'data')
    assert isinstance(response.data, list)


@pytest.mark.unit
def test_currency_exchange_rate_viewset_convert(exchange_rate):
    viewset = CurrencyExchangeRateViewSet()
    viewset.viewset_factory = Mock()
    viewset.viewset_factory.create.return_value = Mock()
    viewset.viewset_factory.create.return_value.convert.return_value = (
        {
            'exchanged_currency': exchange_rate.exchanged_currency,
            'exchanged_amount': round(random.uniform(10, 100), 2),
            'rate_value': round(random.uniform(0.5, 1.5), 6)
        },
        HTTPStatus.OK.value
    )
    request = RequestFactory()
    request.query_params = {
        'source_currency': exchange_rate.source_currency,
        'exchanged_currency': exchange_rate.exchanged_currency,
        'amount': round(random.uniform(10, 100), 2)
    }
    response = viewset.convert(request)
    assert hasattr(response, 'status_code')
    assert response.status_code == HTTPStatus.OK.value
    assert hasattr(response, 'data')
    assert isinstance(response.data, dict)


@pytest.mark.unit
def test_currency_exchange_rate_viewset_list(exchange_rate):
    series_length = random.randint(1, 10)
    viewset = CurrencyExchangeRateViewSet()
    viewset.viewset_factory = Mock()
    viewset.viewset_factory.create.return_value = Mock()
    viewset.viewset_factory.create.return_value.list.return_value = (
        [exchange_rate for _ in range(series_length)],
        HTTPStatus.OK.value
    )
    request = RequestFactory()
    request.query_params = {
        'source_currency': exchange_rate.source_currency,
        'date_from': (
            datetime.date.today() + datetime.timedelta(days=-series_length)
        ).strftime('%Y-%m-%d'),
        'date_to': datetime.date.today().strftime('%Y-%m-%d'),
    }
    response = viewset.list(request)
    assert hasattr(response, 'status_code')
    assert response.status_code == HTTPStatus.OK.value
    assert hasattr(response, 'data')
    assert isinstance(response.data, list)


@pytest.mark.unit
def test_currency_exchange_rate_viewset_calculate_twr(exchange_rate):
    viewset = CurrencyExchangeRateViewSet()
    viewset.viewset_factory = Mock()
    viewset.viewset_factory.create.return_value = Mock()
    viewset.viewset_factory.create.return_value.calculate_twr.return_value = (
        {'time_weighted_rate': round(random.uniform(0.5, 1.5), 6)},
        HTTPStatus.OK.value
    )
    request = RequestFactory()
    request.query_params = {
        'source_currency': exchange_rate.source_currency,
        'exchanged_currency': exchange_rate.exchanged_currency,
        'date_from': (
            datetime.date.today() + datetime.timedelta(days=-5)
        ).strftime('%Y-%m-%d'),
        'date_to': datetime.date.today().strftime('%Y-%m-%d'),
    }
    response = viewset.calculate_twr(request)
    assert hasattr(response, 'status_code')
    assert response.status_code == HTTPStatus.OK.value
    assert hasattr(response, 'data')
    assert isinstance(response.data, dict)
