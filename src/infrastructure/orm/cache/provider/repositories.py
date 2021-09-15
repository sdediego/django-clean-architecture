# coding: utf-8

from typing import List

from django.core.cache import cache

from src.domain.provider import ProviderEntity
from src.infrastructure.orm.cache.provider.constants import (
    CACHE_PROVIDERS_BY_PRIORITY_KEY)


class ProviderCacheRepository:

    def get_by_priority(self) -> List[ProviderEntity]:
        return cache.get(CACHE_PROVIDERS_BY_PRIORITY_KEY)

    def save(self, providers: List[ProviderEntity]):
        cache.set(CACHE_PROVIDERS_BY_PRIORITY_KEY, providers)
