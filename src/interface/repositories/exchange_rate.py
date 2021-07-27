# coding: utf-8

from django.db.models.query import QuerySet

from src.domain.exchange_rate import CurrencyEntity, CurrencyExchangeRateEntity


class CurrencyRepository:

    def __init__(self, db_repo: object):
        self.db_repo = db_repo

    def get(self, code: str) -> CurrencyEntity:
        return self.db_repo.get(code)

    def get_availables(self) -> QuerySet[CurrencyEntity]:
        return self.db_repo.get_availables()


class CurrencyExchangeRateRepository:

    def __init__(self, db_repo: object):
        self.db_repo = db_repo

    def get(self, source_currency: str, exchanged_currency: str,
            valuation_date: str) -> CurrencyExchangeRateEntity:
        return self.db_repo.get(source_currency, exchanged_currency, valuation_date)

    def get_rate_series(self, source_currency: str, exchanged_currency: str,
            date_from: str, date_to: str) -> QuerySet[CurrencyExchangeRateEntity]:
        return self.db_repo.get_time_series(
            source_currency, exchanged_currency, date_from, date_to)

    def get_time_series(self, source_currency: str, exchanged_currency: str,
            date_from: str, date_to: str) -> QuerySet[CurrencyExchangeRateEntity]:
        return self.db_repo.get_time_series(
            source_currency, exchanged_currency, date_from, date_to)
