# coding: utf-8

import random

import pytest

from src.domain.provider import ProviderEntity, ProviderSettingEntity
from src.infrastructure.orm.db.provider.repositories import ProviderDatabaseRepository
from tests.infrastructure.orm.db.factories.provider import (
    ProviderFactory, ProviderSettingFactory)


@pytest.mark.django_db
def test_provider_db_repository_get_by_priority():
    batch_size = random.randint(1, 5)
    provider = ProviderFactory.create()
    provider_settings = ProviderSettingFactory.create_batch(
        batch_size, provider=provider)
    result = ProviderDatabaseRepository().get_by_priority()
    assert isinstance(result, list)
    assert all([isinstance(provider, ProviderEntity) for provider in result])
    assert all([isinstance(setting, ProviderSettingEntity)
                for _, setting in result[0].settings.items()])
    assert len(provider_settings) == len(result[0].settings)
    assert ProviderEntity.to_string(result[0]) == str(provider)
