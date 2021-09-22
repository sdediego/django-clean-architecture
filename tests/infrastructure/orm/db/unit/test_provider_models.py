# coding: utf-8

import pytest

from src.domain.constants import (
    BOOLEAN_SETTING_TYPE, FLOAT_SETTING_TYPE, INTEGER_SETTING_TYPE,
    SECRET_SETTING_TYPE, TEXT_SETTING_TYPE, URL_SETTING_TYPE)
from src.domain.provider import ProviderEntity, ProviderSettingEntity
from src.infrastructure.orm.db.provider.models import (
    Provider, ProviderSetting)
from tests.fixtures import provider, provider_setting


def create_provider_model(provider):
    return Provider(
        name=provider.name,
        driver=provider.driver,
        priority=provider.priority,
        enabled=provider.enabled
    )


def create_provider_settings_model(provider, provider_setting):
    return ProviderSetting(
        provider=create_provider_model(provider),
        setting_type=provider_setting.setting_type,
        key=provider_setting.key,
        value=provider_setting.value,
        description=provider_setting.description
    )


@pytest.mark.unit
def test_provider_attrs(provider):
    model = create_provider_model(provider)
    assert isinstance(model, Provider)
    assert isinstance(model.name, str)
    assert isinstance(model.driver, str)
    assert isinstance(model.priority, int)
    assert isinstance(model.enabled, bool)


@pytest.mark.unit
def test_provider_representation(provider):
    model = create_provider_model(provider)
    assert str(model) == ProviderEntity.to_string(provider)


@pytest.mark.unit
def test_provider_setting_attrs(provider, provider_setting):
    model = create_provider_settings_model(provider, provider_setting)
    assert isinstance(model, ProviderSetting)
    assert isinstance(model.provider, Provider)
    assert isinstance(model.setting_type, str)
    assert isinstance(model.key, str)
    assert isinstance(model.description, str)

    if model.setting_type == BOOLEAN_SETTING_TYPE:
        assert isinstance(model.value, bool)
    elif model.setting_type == INTEGER_SETTING_TYPE:
        assert isinstance(model.value, int)
    elif model.setting_type == FLOAT_SETTING_TYPE:
        assert isinstance(model.value, float)
    elif model.setting_type == SECRET_SETTING_TYPE:
        assert isinstance(model.value, str)
    elif model.setting_type in (TEXT_SETTING_TYPE, URL_SETTING_TYPE):
        assert isinstance(model.value, str)


@pytest.mark.unit
def test_provider_setting_representation(provider, provider_setting):
    model = create_provider_settings_model(provider, provider_setting)
    assert str(model) == ProviderSettingEntity.to_string(provider_setting)
