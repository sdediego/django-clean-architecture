# coding: utf-8

import pytest

from src.domain.constants import (
    BOOLEAN_SETTING_TYPE, FLOAT_SETTING_TYPE, INTEGER_SETTING_TYPE,
    SECRET_SETTING_TYPE, TEXT_SETTING_TYPE, URL_SETTING_TYPE)
from src.domain.provider import ProviderEntity, ProviderSettingEntity
from tests.fixtures import provider, provider_setting


@pytest.mark.unit
def test_provider_entity_attrs(provider):
    assert isinstance(provider.name, str)
    assert isinstance(provider.driver, str)
    assert isinstance(provider.priority, int)
    assert isinstance(provider.enabled, bool)
    assert isinstance(provider.settings, dict)


@pytest.mark.unit
def test_provider_entity_representation(provider):
    entity_str = ProviderEntity.to_string(provider)
    assert isinstance(entity_str, str)
    assert provider.name in entity_str
    assert provider.driver in entity_str
    assert str(provider.priority) in entity_str


@pytest.mark.unit
def test_provider_setting_entity_attrs(provider_setting):
    assert isinstance(provider_setting.provider, ProviderEntity)
    assert isinstance(provider_setting.setting_type, str)
    assert isinstance(provider_setting.key, str)
    assert isinstance(provider_setting.description, str)


@pytest.mark.unit
def test_provider_setting_entity_post_init(provider_setting):
    if provider_setting.setting_type == BOOLEAN_SETTING_TYPE:
        assert isinstance(provider_setting.value, bool)
    elif provider_setting.setting_type == INTEGER_SETTING_TYPE:
        assert isinstance(provider_setting.value, int)
    elif provider_setting.setting_type == FLOAT_SETTING_TYPE:
        assert isinstance(provider_setting.value, float)
    elif provider_setting.setting_type == SECRET_SETTING_TYPE:
        assert isinstance(provider_setting.value, str)
    elif provider_setting.setting_type in (TEXT_SETTING_TYPE, URL_SETTING_TYPE):
        assert isinstance(provider_setting.value, str)


@pytest.mark.unit
def test_provider_setting_entity_encode_and_decode_secret(provider):
    secret_value = 'secret_value'
    encoded_secret_value = ProviderSettingEntity.encode_secret(secret_value)
    provider_setting = ProviderSettingEntity(
        provider=provider,
        setting_type=SECRET_SETTING_TYPE,
        key='secret_key',
        value=encoded_secret_value
    )

    assert isinstance(provider_setting.value, str)
    assert provider_setting.value == secret_value


@pytest.mark.unit
def test_provider_setting_entity_representation(provider_setting):
    entity_str = ProviderSettingEntity.to_string(provider_setting)
    value = provider_setting.value
    if provider_setting.setting_type == SECRET_SETTING_TYPE:
        value = '*' * 10

    assert isinstance(entity_str, str)
    assert str(provider_setting.provider.name) in entity_str
    assert provider_setting.key in entity_str
    assert str(value) in entity_str
