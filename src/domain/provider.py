# coding: utf-8

import base64
from dataclasses import dataclass, field

from src.domain.constants import (
    BOOLEAN_SETTING_TYPE, FLOAT_SETTING_TYPE, INTEGER_SETTING_TYPE,
    SECRET_SETTING_TYPE, TEXT_SETTING_TYPE, URL_SETTING_TYPE)


@dataclass
class ProviderEntity:
    name: str = None
    slug: str = None
    priority: int = None
    enabled: bool = None
    settings: dict = field(default_factory=dict)

    @staticmethod
    def to_string(provider: 'ProviderEntity') -> str:
        return f'{provider.name} ({provider.slug}): Priority {provider.priority}'


@dataclass
class ProviderSettingEntity:
    provider: ProviderEntity = None
    setting_type: str = None
    key: str = None
    value: str = None
    description: str = None

    def __post_init__(self):
        if self.setting_type == BOOLEAN_SETTING_TYPE:
            self.value = self.value == 'True'
        elif self.setting_type == INTEGER_SETTING_TYPE:
            self.value = int(self.value)
        elif self.setting_type == FLOAT_SETTING_TYPE:
            self.value = float(self.value)
        elif self.setting_type == SECRET_SETTING_TYPE:
            self.value = base64.decodebytes(self.value.encode()).decode()
        elif self.setting_type in (TEXT_SETTING_TYPE, URL_SETTING_TYPE):
            self.value = str(self.value)

    @staticmethod
    def to_string(setting: 'ProviderSettingEntity') -> str:
        value = setting.value
        if setting.setting_type == SECRET_SETTING_TYPE:
            value = '*' * 10
        return f'{setting.provider} - {setting.key}: {value}'
