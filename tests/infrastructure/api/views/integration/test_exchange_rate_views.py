# coding: utf-8

import datetime
import random
import urllib
from http import HTTPStatus
from unittest.mock import Mock, patch

from django.urls import reverse

from src.infrastructure.orm.db.exchange_rate.models import (
    Currency, CurrencyExchangeRate)
from tests.fixtures import currency, exchange_rate


@patch.object(Currency, 'objects')
def test_currency_viewset_get(mock_objets, currency, client):
    mock_filter = mock_objets.filter
    mock_filter.return_value = Mock()
    mock_values = mock_filter.return_value.values
    mock_values.return_value = Mock()
    mock_first = mock_values.return_value.first
    mock_first.return_value = vars(currency)
    url = reverse('api:currencies-get', kwargs={'code': currency.code})
    response = client.get(url)
    assert mock_first.called
    assert hasattr(response, 'status_code')
    assert response.status_code == HTTPStatus.OK.value
    assert hasattr(response, 'data')
    assert isinstance(response.data, dict)


@patch.object(Currency, 'objects')
def test_currency_viewset_get_entity_does_not_exist(mock_objets, client):
    mock_filter = mock_objets.filter
    mock_filter.return_value = Mock()
    mock_values = mock_filter.return_value.values
    mock_values.return_value = Mock()
    mock_first = mock_values.return_value.first
    mock_first.return_value = None
    url = reverse('api:currencies-get', kwargs={'code': 'code'})
    response = client.get(url)
    assert mock_first.called
    assert hasattr(response, 'status_code')
    assert response.status_code == HTTPStatus.NOT_FOUND.value
    assert hasattr(response, 'data')
    assert isinstance(response.data, dict)
    assert 'error' in response.data


@patch.object(Currency, 'objects')
def test_currency_viewset_list(mock_objets, currency, client):
    num_of_currencies = random.randint(1, 10)
    mock_values = mock_objets.values
    mock_values.return_value = [vars(currency) for _ in range(num_of_currencies)]
    url = reverse('api:currencies-list')
    response = client.get(url)
    assert mock_values.called
    assert hasattr(response, 'status_code')
    assert response.status_code == HTTPStatus.OK.value
    assert hasattr(response, 'data')
    assert isinstance(response.data, list)


@patch.object(CurrencyExchangeRate, 'objects')
def test_exchange_rate_viewset_convert(mock_objets, exchange_rate, client):
    mock_filter = mock_objets.filter
    mock_filter.return_value = Mock()
    mock_values = mock_filter.return_value.values
    mock_values.return_value = Mock()
    mock_first = mock_values.return_value.first
    mock_first.return_value = vars(exchange_rate)
    params = {
        'source_currency': exchange_rate.source_currency,
        'exchanged_currency': exchange_rate.exchanged_currency,
        'amount': round(random.uniform(10, 100), 2)
    }
    url = f'{reverse("api:exchange-rate-convert")}?{urllib.parse.urlencode(params)}'
    response = client.get(url)
    assert mock_first.called
    assert hasattr(response, 'status_code')
    assert response.status_code == HTTPStatus.OK.value
    assert hasattr(response, 'data')
    assert isinstance(response.data, dict)


@patch.object(CurrencyExchangeRate, 'objects')
def test_exchange_rate_viewset_convert_errors(mock_objets, exchange_rate, client):
    mock_filter = mock_objets.filter
    mock_filter.return_value = Mock()
    mock_values = mock_filter.return_value.values
    mock_values.return_value = Mock()
    mock_first = mock_values.return_value.first
    mock_first.return_value = None
    params = {
        'source_currency': exchange_rate.source_currency,
        'exchanged_currency': exchange_rate.exchanged_currency,
        'amount': 'amount'
    }
    url = f'{reverse("api:exchange-rate-convert")}?{urllib.parse.urlencode(params)}'
    response = client.get(url)
    assert not mock_first.called
    assert hasattr(response, 'status_code')
    assert response.status_code == HTTPStatus.BAD_REQUEST.value
    assert hasattr(response, 'data')
    assert isinstance(response.data, dict)
    assert 'errors' in response.data


@patch.object(CurrencyExchangeRate, 'objects')
def test_exchange_rate_viewset_convert_entity_does_not_exist(mock_objets, exchange_rate, client):
    mock_filter = mock_objets.filter
    mock_filter.return_value = Mock()
    mock_values = mock_filter.return_value.values
    mock_values.return_value = Mock()
    mock_first = mock_values.return_value.first
    mock_first.return_value = None
    params = {
        'source_currency': 'code',
        'exchanged_currency': exchange_rate.exchanged_currency,
        'amount': round(random.uniform(10, 100), 2)
    }
    url = f'{reverse("api:exchange-rate-convert")}?{urllib.parse.urlencode(params)}'
    response = client.get(url)
    assert mock_first.called
    assert hasattr(response, 'status_code')
    assert response.status_code == HTTPStatus.NOT_FOUND.value
    assert hasattr(response, 'data')
    assert isinstance(response.data, dict)
    assert 'error' in response.data


@patch.object(CurrencyExchangeRate, 'objects')
def test_exchange_rate_viewset_list(mock_objets, exchange_rate, client):
    num_of_rates = random.randint(1, 10)
    mock_filter = mock_objets.filter
    mock_filter.return_value = Mock()
    mock_values = mock_filter.return_value.values
    mock_values.return_value = [vars(exchange_rate) for _ in range(num_of_rates)]
    params = {
        'source_currency': exchange_rate.source_currency,
        'date_from': datetime.date.today() + datetime.timedelta(days=-num_of_rates),
        'date_to': datetime.date.today()
    }
    url = f'{reverse("api:exchange-rate-list")}?{urllib.parse.urlencode(params)}'
    response = client.get(url)
    assert mock_values.called
    assert hasattr(response, 'status_code')
    assert response.status_code == HTTPStatus.OK.value
    assert hasattr(response, 'data')
    assert isinstance(response.data, list)


@patch.object(CurrencyExchangeRate, 'objects')
def test_exchange_rate_viewset_list_errors(mock_objets, exchange_rate, client):
    mock_filter = mock_objets.filter
    mock_filter.return_value = Mock()
    mock_values = mock_filter.return_value.values
    mock_values.return_value = None
    params = {
        'source_currency': exchange_rate.source_currency,
        'date_to': datetime.date.today(),
    }
    url = f'{reverse("api:exchange-rate-list")}?{urllib.parse.urlencode(params)}'
    response = client.get(url)
    assert not mock_values.called
    assert hasattr(response, 'status_code')
    assert response.status_code == HTTPStatus.BAD_REQUEST.value
    assert hasattr(response, 'data')
    assert isinstance(response.data, dict)
    assert 'errors' in response.data


@patch.object(CurrencyExchangeRate, 'objects')
def test_exchange_rate_viewset_calculate_twr(mock_objets, exchange_rate, client):
    num_of_rates = random.randint(1, 10)
    mock_filter = mock_objets.filter
    mock_filter.return_value = Mock()
    mock_values_list = mock_filter.return_value.values_list
    mock_values_list.return_value = [
        round(random.uniform(0.5, 1.5), 6) for _ in range(num_of_rates)]
    params = {
        'source_currency': exchange_rate.source_currency,
        'exchanged_currency': exchange_rate.exchanged_currency,
        'date_from': datetime.date.today() + datetime.timedelta(days=-num_of_rates),
        'date_to': datetime.date.today(),
    }
    url = f'{reverse("api:exchange-rate-calculate-twr")}?{urllib.parse.urlencode(params)}'
    response = client.get(url)
    assert mock_values_list.called
    assert hasattr(response, 'status_code')
    assert response.status_code == HTTPStatus.OK.value
    assert hasattr(response, 'data')
    assert isinstance(response.data, dict)


@patch.object(CurrencyExchangeRate, 'objects')
def test_exchange_rate_viewset_calculate_twr_errors(mock_objets, exchange_rate, client):
    mock_filter = mock_objets.filter
    mock_filter.return_value = Mock()
    mock_values_list = mock_filter.return_value.values_list
    mock_values_list.return_value = None
    params = {
        'source_currency': exchange_rate.source_currency,
        'exchanged_currency': exchange_rate.exchanged_currency,
        'date_to': datetime.date.today(),
    }
    url = f'{reverse("api:exchange-rate-calculate-twr")}?{urllib.parse.urlencode(params)}'
    response = client.get(url)
    assert not mock_values_list.called
    assert hasattr(response, 'status_code')
    assert response.status_code == HTTPStatus.BAD_REQUEST.value
    assert hasattr(response, 'data')
    assert isinstance(response.data, dict)
    assert 'errors' in response.data
