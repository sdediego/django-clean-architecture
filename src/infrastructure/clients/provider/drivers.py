# coding: utf-8

from http import HTTPStatus
from importlib import import_module
from typing import Any, List

from src.domain.provider import ProviderEntity
from src.infrastructure.clients.provider.base import ProviderBaseDriver
from src.usecases.provider import ProviderInteractor


class ProviderMasterDriver:
    ACTIONS = {
        'currency_get': 'get_currencies',
        'currency_list': 'get_currencies',
        'exchange_rate_calculate_twr': 'get_time_series',
        'exchange_rate_convert': 'get_exchange_rate',
        'exchange_rate_list': 'get_time_series',
    }

    def __init__(self, provider_interactor: ProviderInteractor):
        self.provider_interactor = provider_interactor

    @property
    def providers(self) -> List[ProviderEntity]:
        return self.provider_interactor.get_by_priority()

    def _get_driver_by_priority(self) -> ProviderBaseDriver:
        for provider in self.providers:
            driver_name = provider.name
            try:
                module = import_module('src.infrastructure.clients.provider')
            except ImportError:
                raise ImportError(f'Unable to import driver {driver_name}')
            driver = getattr(module, f'{driver_name}Driver')
            yield driver(provider)

    def fetch_data(self, action: str, **kwargs: dict) -> Any:
        error = 'Unable to fetch data from remote server'
        for driver in self._get_driver_by_priority():
            method = getattr(driver, self.ACTIONS.get(action, None))
            try:
                response = method(**kwargs)
            except Exception as err:
                error = err
            else:
                if response:
                    break
        else:
            response = {
                'error': error.message if hasattr(
                    error, 'message') else str(error),
                'status_code': error.code if hasattr(
                    error, 'code') else HTTPStatus.INTERNAL_SERVER_ERROR.value
            }
        return response
