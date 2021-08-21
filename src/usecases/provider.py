# coding: utf-8

from typing import List

from src.domain.provider import ProviderEntity


class ProviderInteractor:

    def __init__(self, provider_repo: object):
        self.provider_repo = provider_repo

    def get_by_priority(self) -> List[ProviderEntity]:
        return self.provider_repo.get_by_priority()
