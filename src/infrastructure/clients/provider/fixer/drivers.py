# coding: utf-8

import datetime
from typing import List

from requests import Response
from requests.exceptions import RequestException

from src.domain.exchange_rate import CurrencyEntity, CurrencyExchangeRateEntity
from src.domain.provider import ProviderEntity
from src.infrastructure.clients.provider.base import ProviderBaseDriver
from src.infrastructure.clients.provider.fixer.exceptions import FixerDriverError
from src.infrastructure.clients.provider.fixer.serializers import (
    CurrencySerializer, ExchangeRateSerializer, TimeSeriesSerializer)


class FixerDriver(ProviderBaseDriver):
    CURRENCIES = 'currencies'
    HISTORICAL_RATE = 'historical'
    TIME_SERIES = 'timeseries'
    ENDPOINTS = {
        CURRENCIES: {
            'method': 'get',
            'path': 'symbols',
            'serializer_class': CurrencySerializer,
        },
        HISTORICAL_RATE: {
            'method': 'get',
            'path': '{date}',
            'serializer_class': ExchangeRateSerializer,
        },
        TIME_SERIES: {
            'method': 'get',
            'path': 'timeseries',
            'serializer_class': TimeSeriesSerializer,
        }
    }

    def __init__(self, provider: ProviderEntity):
        super().__init__(provider)
        self.api_url = provider.settings.get('api_url').value
        self.access_key = provider.settings.get('access_key').value

    def _add_access_key(self, params: dict) -> dict:
        params = params or {}
        params.update({'access_key': self.access_key})
        return params

    def _build_request(self, endpoint: str, data: dict, params: dict,
                       url_params: dict) -> dict:
        params = self._add_access_key(params)
        return super()._build_request(endpoint, data, params, url_params)

    def _has_response_error(self, response: Response) -> bool:
        try:
            data = response.json()
        except ValueError:
            return False
        return data.get('error') is not None

    def _handle_response_error(self, error: RequestException):
        has_response = error.response is not None
        message = error.response.reason if has_response else str(error)
        status_code = error.response.status_code if has_response else None
        raise FixerDriverError(message=message, code=status_code)

    def _process_response_error(self, data: dict, status_code: int):
        message = data.get('error', {}).get('info') if data else ''
        raise FixerDriverError(message=message, code=status_code)

    def get_currencies(self) -> List[CurrencyEntity]:
        response = self._request(self.CURRENCIES)
        currencies = self._deserialize_response(self.CURRENCIES, response)
        return currencies

    def get_exchange_rate(self, source_currency: str, exchanged_currency: str,
                          date: str = None) -> CurrencyExchangeRateEntity:
        url_params = {'date': date or datetime.date.today().strftime('%Y-%m-%d')}
        params = {'base': source_currency, 'symbols': exchanged_currency}
        response = self._request(self.HISTORICAL_RATE, params=params, url_params=url_params)
        exchange_rate = self._deserialize_response(self.HISTORICAL_RATE, response)
        return exchange_rate

    def get_time_series(self, source_currency: str, exchanged_currency: str,
                        date_from: str, date_to: str) -> List[CurrencyExchangeRateEntity]:
        params = {
            'base': source_currency,
            'symbols': exchanged_currency,
            'start_date': date_from,
            'end_date': date_to,
        }
        response = self._request(self.TIME_SERIES, params=params)
        timeseries = self._deserialize_response(self.TIME_SERIES, response)
        return timeseries
