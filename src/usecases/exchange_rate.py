# coding: utf-8

from typing import List

import pandas as pd

from django.db.models.query import QuerySet

from src.domain.exchange_rate import CurrencyEntity, CurrencyExchangeRateEntity


class CurrencyInteractor:

    def __init__(self, currency_repo: object):
        self.currency_repo = currency_repo

    def get(self, code: str) -> CurrencyEntity:
        return self.currency_repo.get(code)

    def get_availables(self) -> QuerySet[CurrencyEntity]:
        return self.currency_repo.get_availables()


class CurrencyExchangeRateInteractor:

    def __init__(self, exchange_rate_repo: object):
        self.exchange_rate_repo = exchange_rate_repo

    def get(self, source_currency: str, exchanged_currency: str,
            valuation_date: str) -> CurrencyExchangeRateEntity:
        return self.exchange_rate_repo.get(
            source_currency, exchanged_currency, valuation_date)

    def get_latest(self, source_currency: str, exchanged_currency: str) \
            -> CurrencyExchangeRateEntity:
        today = pd.Timestamp.today().strftime('%Y-%m-%d')
        return self.get(source_currency, exchanged_currency, today)

    def get_rate_series(self, source_currency: str, exchanged_currency: str,
            date_from: str, date_to: str) -> List[float]:
        return self.exchange_rate_repo.get_rate_series(
            source_currency, exchanged_currency, date_from, date_to)

    def get_time_series(self, source_currency: str, exchanged_currency: str,
            date_from: str, date_to: str) -> QuerySet[CurrencyExchangeRateEntity]:
        return self.exchange_rate_repo.get_time_series(
            source_currency, exchanged_currency, date_from, date_to)

    def get_all_time_series(self, source_currency: str, date_from: str,
            date_to: str) -> QuerySet[CurrencyExchangeRateEntity]:
        return self.get_time_series(source_currency, None, date_from, date_to)
