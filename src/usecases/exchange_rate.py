# coding: utf-8

from django.db.models.query import QuerySet

from src.domain.exchange_rate import CurrencyEntity


class CurrencyInteractor:

    def __init__(self, currency_repo: object):
        self.currency_repo = currency_repo

    def get(self, code: str) -> CurrencyEntity:
        return self.currency_repo.get(code)

    def get_availables(self) -> QuerySet[CurrencyEntity]:
        return self.currency_repo.get_availables()
