# coding: utf-8

from typing import List, Union

from django.core.cache import cache

from src.domain.exchange_rate import CurrencyEntity
from src.infrastructure.orm.cache.exchange_rate.constants import (
    CACHE_AVAILABLE_CURRENCIES_KEY)


class CurrencyCacheRepository:

    def get(self, key: str) -> CurrencyEntity:
        return cache.get(key)

    def get_availables(self) -> List[CurrencyEntity]:
        return self.get(CACHE_AVAILABLE_CURRENCIES_KEY)

    def save(self, key: str, value: Union[CurrencyEntity, list]):
        cache.set(key, value)

    def save_availables(self, currencies: List[CurrencyEntity]):
        self.save(CACHE_AVAILABLE_CURRENCIES_KEY, currencies)
