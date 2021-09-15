# coding: utf-8

import random
import string

import factory
from factory import django, fuzzy

from src.domain.constants import (
    BOOLEAN_SETTING_TYPE, FLOAT_SETTING_TYPE, INTEGER_SETTING_TYPE,
    SECRET_SETTING_TYPE, TEXT_SETTING_TYPE, URL_SETTING_TYPE)
from src.domain.provider import ProviderSettingEntity
from src.infrastructure.orm.db.provider.models import (
    Provider, ProviderSetting)
from tests.fixtures import generate_random_string


setting_type, value = random.choice([
    (BOOLEAN_SETTING_TYPE, random.choice(['True', 'False'])),
    (INTEGER_SETTING_TYPE, str(random.randint(1, 99))),
    (FLOAT_SETTING_TYPE, str(random.uniform(1.00, 99.99))),
    (SECRET_SETTING_TYPE, ProviderSettingEntity.encode_secret('secret')),
    (TEXT_SETTING_TYPE, generate_random_string(10)),
    (URL_SETTING_TYPE, generate_random_string(10)),
])


class ProviderFactory(django.DjangoModelFactory):

    class Meta:
        model = Provider

    name = fuzzy.FuzzyText(length=15, chars=string.ascii_letters)
    slug = fuzzy.FuzzyText(length=15, chars=string.ascii_lowercase)
    priority = fuzzy.FuzzyInteger(low=1, high=10)
    enabled = True


class ProviderSettingFactory(django.DjangoModelFactory):

    class Meta:
        model = ProviderSetting

    provider = factory.SubFactory(ProviderFactory)
    setting_type = setting_type
    key = fuzzy.FuzzyText(length=15, chars=string.ascii_lowercase)
    value = value
    description = fuzzy.FuzzyText(length=50, chars=string.ascii_letters)
