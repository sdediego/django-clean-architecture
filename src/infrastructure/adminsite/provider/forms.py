# coding: utf-8

import base64

from django.core.validators import URLValidator
from django.forms import ModelForm, ValidationError

from src.domain.constants import SECRET_SETTING_TYPE
from src.infrastructure.orm.db.provider.models import ProviderSetting


class ProviderSettingForm(ModelForm):

    class Meta:
        model = ProviderSetting
        fields = ('provider', 'setting_type', 'key', 'value', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial.get('setting_type') == SECRET_SETTING_TYPE:
            self.initial['value'] = '*' * 10

    def clean(self):
        super().clean()
        method_name = f'_clean_{self.cleaned_data.get("setting_type")}'
        method = getattr(self, method_name)
        method(self.cleaned_data.get('value'))

    def _clean_secret(self, value: str):
        try:
            str(value)
        except (TypeError, ValueError):
            raise ValidationError(f'{value} value must be string')

    def _clean_text(self, value: str):
        try:
            str(value)
        except (TypeError, ValueError):
            raise ValidationError(f'{value} value must be string')

    def _clean_integer(self, value: int):
        try:
            int(value)
        except (TypeError, ValueError):
            raise ValidationError(f'{value} value must be integer')

    def _clean_float(self, value: float):
        try:
            float(value)
        except (TypeError, ValueError):
            raise ValidationError(f'{value} value must be float')

    def _clean_boolean(self, value: bool):
        if value not in ('True', 'False'):
            raise ValidationError(
                f'{value} value must be either True or False')

    def _clean_url(self, value: str):
        url_validator = URLValidator()
        try:
            url_validator(value)
        except ValidationError:
            raise ValidationError(f'{value} must be a valid absolute url')

    def save(self, commit: bool = True):
        if self.cleaned_data.get('setting_type') == SECRET_SETTING_TYPE \
                and 'value' in self.changed_data:
            self.instance.value = base64.encodebytes(
                self.cleaned_data.get('value').encode()).decode()
        return super().save(commit)
