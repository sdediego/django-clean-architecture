# coding: utf-8

from typing import Any, List

from src.domain.provider import ProviderEntity


class ProviderInteractor:

    def __init__(self, provider_repo: object):
        self.provider_repo = provider_repo

    def get_by_priority(self) -> List[ProviderEntity]:
        return self.provider_repo.get_by_priority()


class ProviderClientInteractor:

    def __init__(self, provider_client: object):
        self.provider_client = provider_client

    def fetch_data(self, action: str, **kwargs: dict) -> Any:
        return self.provider_client.fetch_data(action, **kwargs)
