# coding: utf-8

from django.contrib import admin

from src.infrastructure.orm.db.provider.models import (
    Provider, ProviderSetting)


class ProviderSettingInline(admin.TabularInline):
    model = ProviderSetting


class ProviderAdmin(admin.ModelAdmin):
    model = Provider
    inlines = [ProviderSettingInline]
    list_display = ('name', 'slug', 'priority')
    ordering = ('name',)
