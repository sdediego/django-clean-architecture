# coding: utf-8

from typing import Any


class ProviderClient:

    def __init__(self, provider_driver: object):
        self.provider_driver = provider_driver

    def fetch_data(self, action: str, **kwargs: dict) -> Any:
        return self.provider_driver.fetch_data(action, **kwargs)
