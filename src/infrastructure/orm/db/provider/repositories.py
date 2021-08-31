# coding: utf-8

from typing import List

from django.db.models import Prefetch

from src.domain.provider import ProviderEntity, ProviderSettingEntity
from src.infrastructure.orm.db.provider.models import Provider, ProviderSetting


class ProviderDatabaseRepository:

    def get_by_priority(self) -> List[ProviderEntity]:
        prefetch = Prefetch('settings', queryset=ProviderSetting.objects.all())
        providers = Provider.objects.prefetch_related(prefetch).filter(enabled=True)
        return [
            ProviderEntity(
                name=provider.name,
                slug=provider.slug,
                priority=provider.priority,
                settings={
                    setting.get('key'): ProviderSettingEntity(**setting)
                    for setting in provider.settings.values('setting_type', 'key', 'value')
                }
            ) for provider in providers
        ]
