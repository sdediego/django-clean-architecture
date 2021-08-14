# coding: utf-8

from django.contrib import admin

from src.infrastructure.adminsite.provider.forms import ProviderSettingForm
from src.infrastructure.orm.db.provider.models import (
    Provider, ProviderSetting)


class ProviderSettingInline(admin.TabularInline):
    model = ProviderSetting
    form = ProviderSettingForm
    extra = 0


class ProviderAdmin(admin.ModelAdmin):
    model = Provider
    inlines = [ProviderSettingInline]
    list_display = ('name', 'slug', 'priority', 'enabled')
    ordering = ('priority',)
