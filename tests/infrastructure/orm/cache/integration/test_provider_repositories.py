# coding: utf-8

import random

from django.core.cache import cache

from src.domain.provider import ProviderEntity
from src.infrastructure.orm.cache.provider.constants import (
    CACHE_PROVIDERS_BY_PRIORITY_KEY)
from src.infrastructure.orm.cache.provider.repositories import ProviderCacheRepository
from tests.fixtures import provider


def test_provider_cache_repository_get_by_priority(provider):
    number_of_providers = random.randint(1, 5)
    providers = [provider for _ in range(number_of_providers)]
    cache.set(CACHE_PROVIDERS_BY_PRIORITY_KEY, providers)
    result = ProviderCacheRepository().get_by_priority()
    assert isinstance(result, list)
    assert len(result) == number_of_providers
    assert all([isinstance(provider, ProviderEntity) for provider in result])


def test_provider_cache_repository_save(provider):
    number_of_providers = random.randint(1, 5)
    providers = [provider for _ in range(number_of_providers)]
    ProviderCacheRepository().save(providers)
    result = cache.get(CACHE_PROVIDERS_BY_PRIORITY_KEY)
    assert isinstance(result, list)
    assert len(result) == number_of_providers
    assert all([isinstance(provider, ProviderEntity) for provider in result])
