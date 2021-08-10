# coding: utf-8

import base64
from dataclasses import dataclass, field
from typing import Union

from marshmallow.exceptions import ValidationError
from marshmallow.validate import URL

from src.domain.constants import (
    BOOLEAN_SETTING_TYPE, FLOAT_SETTING_TYPE, INTEGER_SETTING_TYPE,
    SECRET_SETTING_TYPE, TEXT_SETTING_TYPE, URL_SETTING_TYPE)


@dataclass
class ProviderEntity:
    name: str = None
    slug: str = None
    priority: int = None
    settings: list = field(default_factory=list)

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

    @staticmethod
    def to_string(setting: 'ProviderSettingEntity') -> str:
        return f'{setting.provider} - {setting.key}: {setting.value}'

    @property
    def pretty_value(self) -> Union[bool, float, int, str]:
        if self.setting_type == SECRET_SETTING_TYPE:
            return self.visible_secret_value()
        return self.get_value()

    def get_value(self) -> Union[bool, float, int, str]:
        value = None
        if self.setting_type == BOOLEAN_SETTING_TYPE:
            value = self.value == 'True'
        elif self.setting_type == FLOAT_SETTING_TYPE:
            value = float(self.value)
        elif self.setting_type == INTEGER_SETTING_TYPE:
            value = int(self.value)
        elif self.setting_type == SECRET_SETTING_TYPE:
            value = base64.decodebytes(self.value.encode()).decode()
        elif self.setting_type in (TEXT_SETTING_TYPE, URL_SETTING_TYPE):
            value = self.value
        return value

    def visible_secret_value(self) -> str:
        return f'{self.value[:2]}******{self.value[-2:]}'

    def clean(self):
        method_name = f'clean_{self.setting_type}'
        method = getattr(self, method_name)
        method()

    def clean_secret(self):
        pass

    def clean_text(self):
        pass

    def clean_int(self):
        try:
            int(self.value)
        except (TypeError, ValueError):
            raise ValidationError(f'{self.value} value must be integer')

    def clean_float(self):
        try:
            float(self.value)
        except (TypeError, ValueError):
            raise ValidationError(f'{self.value} value must be float')

    def clean_boolean(self):
        if self.value not in ('True', 'False'):
            raise ValidationError(f'{self.value} value must be either True or False')

    def clean_url(self):
        url_validator = URL()
        try:
            url_validator(self.value)
        except ValidationError:
            raise ValidationError(f'{self.value} must be a valid absolute url')

    def pre_save(self) -> 'ProviderSettingEntity':
        if self.setting_type == SECRET_SETTING_TYPE:
            self.value = base64.encodebytes(self.value.encode()).decode()
        return self
