# coding: utf-8

from django.contrib import admin

from src.infrastructure.adminsite.provider.admin import ProviderAdmin
from src.infrastructure.orm.db.provider.models import Provider


admin.site.register(Provider, ProviderAdmin)
