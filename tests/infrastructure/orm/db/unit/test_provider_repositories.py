# coding: utf-8

from unittest.mock import patch

import pytest

from src.domain.provider import ProviderEntity
from src.infrastructure.orm.db.provider.models import Provider, ProviderSetting
from src.infrastructure.orm.db.provider.repositories import ProviderDatabaseRepository
from tests.infrastructure.orm.db.factories.provider import (
    ProviderFactory, ProviderSettingFactory)


@pytest.mark.unit
@patch.object(Provider, 'objects')
@patch.object(ProviderSetting, 'objects')
def test_provider_db_repository_get_by_priority(mock_setting_objects,
                                                mock_provider_objects):
    provider = ProviderFactory.build()
    provider_settings = ProviderSettingFactory.build_batch(2, provider=provider)
    mock_provider_filter = mock_provider_objects.filter
    mock_provider_filter.return_value = [provider]
    mock_settings_all = mock_setting_objects.all
    mock_settings_all.return_value = provider_settings
    result = ProviderDatabaseRepository().get_by_priority()
    assert isinstance(result, list)
    assert all([isinstance(provider, ProviderEntity) for provider in result])
