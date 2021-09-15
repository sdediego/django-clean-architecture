# coding: utf-8

import random
from unittest.mock import patch

from django.core.cache import cache

import pytest

from src.domain.provider import ProviderEntity
from src.infrastructure.orm.cache.provider.repositories import ProviderCacheRepository
from tests.fixtures import provider


@pytest.mark.unit
@patch.object(cache, 'get')
def test_provider_cache_repository_get_by_priority(mock_get, provider):
    number_of_providers = random.randint(1, 5)
    mock_get.return_value = [provider for _ in range(number_of_providers)]
    result = ProviderCacheRepository().get_by_priority()
    assert mock_get.called
    assert isinstance(result, list)
    assert all([isinstance(provider, ProviderEntity) for provider in result])


@pytest.mark.unit
@patch.object(cache, 'set')
def test_provider_cache_repository_save(mock_set, provider):
    mock_set.return_value = None
    number_of_providers = random.randint(1, 5)
    providers = [provider for _ in range(number_of_providers)]
    result = ProviderCacheRepository().save(providers)
    assert mock_set.called
    assert result is None
