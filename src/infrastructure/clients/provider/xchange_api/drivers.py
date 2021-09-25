# coding: utf-8

import asyncio
import json
from itertools import chain, repeat
from typing import List

from requests import Response
from requests.exceptions import RequestException

from src.domain.exchange_rate import CurrencyEntity, CurrencyExchangeRateEntity
from src.domain.provider import ProviderEntity
from src.infrastructure.clients.provider.base import ProviderBaseDriver
from src.infrastructure.clients.provider.decorators import async_event_loop
from src.infrastructure.clients.provider.utils import (
    get_business_days, get_last_business_day)
from src.infrastructure.clients.provider.xchange_api.exceptions import (
    XChangeAPIDriverError)
from src.infrastructure.clients.provider.xchange_api.serializers import (
    ExchangeRateSerializer)


class XChangeAPIDriver(ProviderBaseDriver):
    HISTORICAL_RATE = 'historical'
    ENDPOINTS = {
        HISTORICAL_RATE: {
            'method': 'get',
            'path': 'historical/{date}',
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
        return data.get('message') is not None

    def _handle_response_error(self, error: RequestException):
        has_response = error.response is not None
        message = error.response.reason if has_response else str(error)
        status_code = error.response.status_code if has_response else None
        raise XChangeAPIDriverError(message=message, code=status_code)

    def _process_response_error(self, data: dict, status_code: int):
        message = data.get('message', '')
        raise XChangeAPIDriverError(message=message, code=status_code)

    def get_currencies(self) -> List[CurrencyEntity]:
        with open('./currencies.json', 'r') as currencies_file:
            data = json.load(currencies_file)
        currencies = data.get('availableCurrencies')
        return list(map(lambda currency: CurrencyEntity(**currency), currencies))

    def get_exchange_rate(self, source_currency: str, exchanged_currency: str,
                          date: str = None) -> CurrencyExchangeRateEntity:
        url_params = {'date': date or get_last_business_day()}
        params = {'base': source_currency}
        response = self._request(self.HISTORICAL_RATE, params=params, url_params=url_params)
        response.update({'symbols': exchanged_currency})
        exchange_rate = self._deserialize_response(self.HISTORICAL_RATE, response)
        return exchange_rate[0] if len(exchange_rate) > 0 else None

    @async_event_loop
    async def get_time_series(self, source_currency: str, exchanged_currency: str,
                              date_from: str, date_to: str) -> List[CurrencyExchangeRateEntity]:
        async def request(endpoint: str, params: dict, url_params: dict) -> dict:
            symbols = params.get('symbols')
            response = self._request(endpoint, params=params, url_params=url_params)
            response.update({'symbols': symbols})
            return response

        business_days = get_business_days(date_from, date_to)
        url_params = [{'date': business_day} for business_day in business_days]
        params = {'base': source_currency, 'symbols': exchanged_currency}
        responses = await asyncio.gather(*list(
            map(request, repeat(self.HISTORICAL_RATE), repeat(params), url_params)))
        timeseries = list(chain(*map(
            self._deserialize_response, repeat(self.HISTORICAL_RATE), responses)))
        return timeseries
