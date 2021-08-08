# coding: utf-8

from dataclasses import dataclass


@dataclass
class ProviderEntity:
    name: str = None
    slug: str = None
    priority: int = None
    settings: list = []

    @staticmethod
    def to_string(provider: 'ProviderEntity') -> str:
        return f'{provider.name} ({provider.slug}): Priority {provider.priority}'
