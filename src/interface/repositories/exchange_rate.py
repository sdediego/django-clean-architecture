# coding: utf-8

from django.db.models.query import QuerySet

from src.domain.exchange_rate import CurrencyEntity


class CurrencyRepository:

    def __init__(self, db_repo: object):
        self.db_repo = db_repo

    def get(self, code: str) -> CurrencyEntity:
        return self.db_repo.get(code)

    def get_availables(self) -> QuerySet[CurrencyEntity]:
        return self.db_repo.get_availables()
