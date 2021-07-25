# coding: utf-8

from django.contrib import admin

from src.infrastructure.orm.db.exchange_rate.models import Currency


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    model = Currency
    list_display = ('code', 'name', 'symbol')
    ordering = ('name',)
