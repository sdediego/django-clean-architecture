# coding: utf-8

from django.contrib import admin

from src.infrastructure.adminsite.exchange_rate.admin import (
    CurrencyAdmin, CurrencyExchangeRateAdmin)
from src.infrastructure.orm.db.exchange_rate.models import (
    Currency, CurrencyExchangeRate)


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(CurrencyExchangeRate, CurrencyExchangeRateAdmin)
