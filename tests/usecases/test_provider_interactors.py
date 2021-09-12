# coding: utf-8

from unittest.mock import Mock

import pytest

from src.domain.provider import ProviderEntity
from src.usecases.provider import ProviderInteractor
from tests.fixtures import provider


@pytest.mark.unit
def test_provider_interactor_get_by_priority(provider):
    provider_repo = Mock()
    provider_repo.get_by_priority.return_value = [provider]
    provider_interactor = ProviderInteractor(provider_repo)
    result = provider_interactor.get_by_priority()
    result_first = result[0]
    assert provider_repo.get_by_priority.called
    assert isinstance(result, list)
    assert isinstance(result_first, ProviderEntity)
    assert result_first.name == provider.name
    assert result_first.slug == provider.slug
    assert result_first.priority == provider.priority
    assert result_first.enabled == provider.enabled
    assert ProviderEntity.to_string(
        result_first) == ProviderEntity.to_string(provider)
