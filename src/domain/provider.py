# coding: utf-8

from dataclasses import dataclass, field


@dataclass
class ProviderEntity:
    name: str = None
    slug: str = None
    priority: int = None
    enabled: bool = None
    settings: list = field(default_factory=list)

    @staticmethod
    def to_string(provider: 'ProviderEntity') -> str:
        return f'{provider.name} ({provider.slug}): Priority {provider.priority}'


@dataclass
class ProviderSettingEntity:
    provider: ProviderEntity = None
    setting_type: str = None
    key: str = None
    value: str = None
    description: str = None

    @staticmethod
    def to_string(setting: 'ProviderSettingEntity') -> str:
        return f'{setting.provider} - {setting.key}: {setting.value}'
