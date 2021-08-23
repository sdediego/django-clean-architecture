# coding: utf-8

from typing import List

from src.domain.provider import ProviderEntity


class ProviderRepository:

    def __init__(self, db_repo: object, cache_repo: object):
        self.db_repo = db_repo
        self.cache_repo = cache_repo

    def get_by_priority(self) -> List[ProviderEntity]:
        providers = self.cache_repo.get_by_priority()
        if not providers:
            providers = self.db_repo.get_by_priority()
            self.cache_repo.save(providers)
        return providers
