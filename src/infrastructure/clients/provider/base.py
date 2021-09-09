# coding: utf-8

from typing import Any, List

import requests
from requests import Response
from requests.exceptions import RequestException
from rest_framework import status

from src.domain.exchange_rate import CurrencyEntity, CurrencyExchangeRateEntity
from src.domain.provider import ProviderEntity


class ProviderBaseDriver:
    HEADERS = {'Accept': 'application/json'}
    ENDPOINTS = {}

    def __init__(self, provider: ProviderEntity):
        self.name = provider.name
        self.priority = provider.priority

    def _get_endpoint_info(self, endpoint: str) -> dict:
        return self.ENDPOINTS.get(endpoint, {})

    def _get_headers(self) -> dict:
        return self.HEADERS

    def _get_url(self, endpoint: str, url_params: dict) -> str:
        path = self._get_endpoint_info(endpoint).get('path')
        url = f'{self.api_url}{path}'
        return url.format(**url_params) if url_params else url

    def _get_data_key(self, endpoint_info: dict) -> str:
        return 'json' if endpoint_info.get('json', False) else 'data'

    def _build_request(self, endpoint: str, data: dict, params: dict,
                       url_params: dict) -> dict:
        endpoint_info = self._get_endpoint_info(endpoint)
        request = {
            'method': endpoint_info.get('method'),
            'url': self._get_url(endpoint, url_params),
            'headers': self._get_headers(),
        }
        if params:
            request.update({'params': params})
        if data:
            data_key = self._get_data_key(endpoint_info)
            request[data_key] = data
        return request

    def _has_response_error(self, response: Response) -> bool:
        raise NotImplementedError

    def _handle_response_error(self, error: RequestException):
        raise NotImplementedError

    def _process_response_error(self, data: dict, status_code: int):
        raise NotImplementedError

    def _process_response(self, response: Response) -> dict:
        data = None
        status_code = response.status_code
        try:
            data = response.json()
        except ValueError as err:
            raise err
        if not status.is_success(status_code) or self._has_response_error(response):
            self._process_response_error(data, status_code)
        return data

    def _request(self, endpoint: str, data: dict = None, params: dict = None,
                 url_params: dict = None) -> dict:
        request = self._build_request(endpoint, data, params, url_params)
        try:
            response = requests.request(**request)
            response.raise_for_status()
        except RequestException as err:
            if not self._has_response_error(err.response):
                self._handle_response_error(err)
        except Exception as err:
            raise err
        return self._process_response(response)

    def _get_serializer_class(self, endpoint: str) -> Any:
        endpoint_info = self._get_endpoint_info(endpoint)
        return endpoint_info.get('serializer_class')

    def _deserialize_response(self, endpoint: str, response: dict) -> Any:
        serializer_class = self._get_serializer_class(endpoint)
        return serializer_class().load(response)

    def get_currencies(self) -> List[CurrencyEntity]:
        raise NotImplementedError

    def get_exchange_rate(self, source_currency: str, exchanged_currency: str,
                          date: str) -> CurrencyExchangeRateEntity:
        raise NotImplementedError

    def get_time_series(self, source_currency: str, exchanged_currency: str,
                        date_from: str, date_to: str) -> List[CurrencyExchangeRateEntity]:
        raise NotImplementedError
