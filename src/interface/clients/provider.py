# coding: utf-8

from typing import Any


class ProviderClient:

    def __init__(self, provider_driver: object):
        self.provider_driver = provider_driver

    def get_exchange_rate_data(self, action: str, **kwargs: dict) -> Any:
        return self.provider_driver.get_exchange_rate_data(
            action, **kwargs)
