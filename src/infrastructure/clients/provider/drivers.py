# coding: utf-8

from importlib import import_module
from typing import Any, List

from src.domain.provider import ProviderEntity
from src.infrastructure.clients.provider.base import ProviderBaseDriver
from src.infrastructure.clients.provider.exceptions import ProviderDriverError
from src.usecases.provider import ProviderInteractor


class ProviderMasterDriver:
    ACTIONS = {
        'currency_get': 'get_currencies',
        'currency_list': 'get_currencies',
        'exchange_rate_calculate_twr': 'get_time_series',
        'exchange_rate_conver': 'get_exchange_rate',
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

    def get_exchange_rate_data(self, action: str, **kwargs: dict) -> Any:
        error = None
        for driver in self._get_driver_by_priority():
            method = getattr(driver, self.ACTIONS.get(action, None))
            try:
                response = method(**kwargs)
            except Exception as err:
                error = err
            else:
                break
        else:
            if error is issubclass(error, ProviderDriverError):
                message, code, status = error.message, error.code, error.status
                raise ProviderDriverError(message, code, status)
            raise error
        return response
