# coding: utf-8

from django.contrib import admin

from src.infrastructure.adminsite.provider.forms import (
    ProviderForm, ProviderSettingForm)
from src.infrastructure.orm.db.provider.models import (
    Provider, ProviderSetting)


class ProviderSettingInline(admin.TabularInline):
    model = ProviderSetting
    form = ProviderSettingForm
    extra = 0


class ProviderAdmin(admin.ModelAdmin):
    model = Provider
    form = ProviderForm
    inlines = [ProviderSettingInline]
    list_display = ('name', 'driver', 'priority', 'enabled')
    ordering = ('priority',)
