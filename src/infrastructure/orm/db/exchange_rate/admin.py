# coding: utf-8

from django.contrib import admin

from src.infrastructure.orm.db.exchange_rate.models import (
    Currency, CurrencyExchangeRate)


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    model = Currency
    list_display = ('code', 'name', 'symbol')
    ordering = ('name',)


@admin.register(CurrencyExchangeRate)
class CurrencyExchangeRateAdmin(admin.ModelAdmin):
    model = CurrencyExchangeRate
    list_display = (
        'source_currency', 'exchanged_currency', 'rate_value', 'valuation_date')
    ordering = ('-valuation_date', 'source_currency')
