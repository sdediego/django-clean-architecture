# coding: utf-8

from django.apps import AppConfig


class ExchangeRateConfig(AppConfig):
    label = 'exchange_rate'
    name = 'src.infrastructure.orm.db.exchange_rate'
    verbose_name = 'Exchange rate'


class ProviderConfig(AppConfig):
    label = 'provider'
    name = 'src.infrastructure.orm.db.provider'
    verbose_name = 'Provider'
