# coding: utf-8

from src.domain.constants import (
    BOOLEAN_SETTING_TYPE, FLOAT_SETTING_TYPE, INTEGER_SETTING_TYPE,
    SECRET_SETTING_TYPE, TEXT_SETTING_TYPE, URL_SETTING_TYPE)


# Provider setting types choices
SETTING_TYPE_CHOICES = (
    (BOOLEAN_SETTING_TYPE, 'boolean'),
    (FLOAT_SETTING_TYPE, 'float'),
    (INTEGER_SETTING_TYPE, 'integer'),
    (SECRET_SETTING_TYPE, 'secret'),
    (TEXT_SETTING_TYPE, 'text'),
    (URL_SETTING_TYPE, 'url')
)
