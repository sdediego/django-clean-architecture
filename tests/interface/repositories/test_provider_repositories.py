# coding: utf-8

from unittest.mock import Mock

import pytest

from src.domain.provider import ProviderEntity
from src.interface.repositories.provider import ProviderRepository
from tests.fixtures import provider


@pytest.mark.unit
def test_provider_repository_database_get_by_priority(provider):
    db_repo = Mock()
    db_repo.get_by_priority.return_value = [provider]
    cache_repo = Mock()
    cache_repo.get_by_priority.return_value = None
    cache_repo.save.return_value = None
    provider_repo = ProviderRepository(db_repo, cache_repo)
    result = provider_repo.get_by_priority()
    result_first = result[0]
    assert cache_repo.get_by_priority.called
    assert cache_repo.save.called
    assert db_repo.get_by_priority.called
    assert isinstance(result, list)
    assert isinstance(result_first, ProviderEntity)
    assert result_first.name == provider.name
    assert result_first.slug == provider.slug
    assert result_first.priority == provider.priority
    assert result_first.enabled == provider.enabled
    assert ProviderEntity.to_string(
        result_first) == ProviderEntity.to_string(provider)
