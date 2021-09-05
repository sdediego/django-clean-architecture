# coding: utf-8

import asyncio
from itertools import repeat
from typing import List

from requests import Response
from requests.exceptions import RequestException

from src.domain.exchange_rate import CurrencyEntity, CurrencyExchangeRateEntity
from src.domain.provider import ProviderEntity
from src.infrastructure.clients.provider.base import ProviderBaseDriver
from src.infrastructure.clients.provider.decorators import async_event_loop
from src.infrastructure.clients.provider.utils import (
    get_business_days, get_last_business_day)
from src.infrastructure.clients.provider.exchange_rate_api.exceptions import (
    ExchangeRateAPIDriverError)
from src.infrastructure.clients.provider.exchange_rate_api.serializers import (
    CurrencySerializer, ExchangeRateSerializer)


class ExchangeRateAPIDriver(ProviderBaseDriver):
    CURRENCIES = 'currencies'
    HISTORICAL_RATE = 'historical'
    ENDPOINTS = {
        CURRENCIES: {
            'method': 'get',
            'path': 'codes/',
            'serializer_class': CurrencySerializer,
        },
        HISTORICAL_RATE: {
            'method': 'get',
            'path': 'history/{currency}/{year}/{month}/{day}/',
            'serializer_class': ExchangeRateSerializer,
        }
    }

    def __init__(self, provider: ProviderEntity):
        super().__init__(provider)
        self.api_url = provider.settings.get('api_url').value
        self.api_key = provider.settings.get('api_key').value

    def _get_headers(self) -> dict:
        headers = super()._get_headers()
        headers.update({'api-key': self.api_key})
        return headers

    def _has_response_error(self, response: Response) -> bool:
        try:
            data = response.json()
        except ValueError:
            return False
        return data.get('error-type') is not None

    def _handle_response_error(self, error: RequestException):
        has_response = error.response is not None
        message = error.response.reason if has_response else str(error)
        status_code = error.response.status_code if has_response else None
        raise ExchangeRateAPIDriverError(message=message, code=status_code)

    def _process_response_error(self, data: dict, status_code: int):
        message = data.get('error-type', '')
        raise ExchangeRateAPIDriverError(message=message, code=status_code)

    def get_currencies(self) -> List[CurrencyEntity]:
        response = self._request(self.CURRENCIES)
        currencies = self._deserialize_response(self.CURRENCIES, response)
        return [CurrencyEntity(**currency) for currency in currencies]

    def get_exchange_rate(self, source_currency: str, exchanged_currency: str,
                          date: str = None) -> CurrencyExchangeRateEntity:
        date = date or get_last_business_day()
        year, month, day = date.split('-')
        url_params = {
            'currency': source_currency,
            'year': year,
            'month': month,
            'day': day,
        }
        response = self._request(self.HISTORICAL_RATE, url_params=url_params)
        response.update({'exchanged_currency': exchanged_currency})
        exchange_rate = self._deserialize_response(self.HISTORICAL_RATE, response)
        return CurrencyExchangeRateEntity(**exchange_rate)

    @async_event_loop
    async def get_time_series(self, source_currency: str, exchanged_currency: str,
                              date_from: str, date_to: str) -> List[CurrencyExchangeRateEntity]:
        async def request(endpoint: str, url_params: dict) -> dict:
            return super()._request(endpoint, url_params=url_params)

        url_params = []
        for business_day in get_business_days(date_from, date_to):
            year, month, day = business_day.split('-')
            url_params.append({
                'currency': source_currency,
                'year': year,
                'month': month,
                'day': day,
            })
        responses = [
            result.update({'exchanged_currency': exchanged_currency})
            async for result in await asyncio.gather(*list(
                map(request, repeat(self.HISTORICAL_RATE), url_params)))
        ]
        timeseries = list(
            map(self._deserialize_response, repeat(self.HISTORICAL_RATE), responses))
        return [
            CurrencyExchangeRateEntity(**exchange_rate) for exchange_rate in timeseries
        ]
