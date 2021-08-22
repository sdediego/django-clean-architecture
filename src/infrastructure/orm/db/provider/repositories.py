# coding: utf-8

from typing import List

from src.domain.provider import ProviderEntity, ProviderSettingEntity
from src.infrastructure.orm.db.provider.models import Provider, ProviderSetting


class ProviderDatabaseRepository:

    def get_by_priority(self) -> List[ProviderEntity]:
        return [
            ProviderEntity(
                name=provider.get('name'),
                slug=provider.get('slug'),
                priority=provider.get('priority'),
                settings={
                    setting.get('key'): ProviderSettingEntity(**setting)
                    for setting in ProviderSetting.objects.filter(
                        provider=provider.get('id')).values('setting_type', 'key', 'value')
                }
            ) for provider in Provider.objects.filter(enabled=True).values()
        ]
