# coding: utf-8

from typing import List

from src.domain.provider import ProviderEntity


class ProviderRepository:

    def __init__(self, db_repo: object):
        self.db_repo = db_repo

    def get_by_priority(self) -> List[ProviderEntity]:
        return self.db_repo.get_by_priority()
