# coding: utf-8

from typing import List

from src.domain.exchange_rate import CurrencyEntity, CurrencyExchangeRateEntity


class CurrencyRepository:

    def __init__(self, db_repo: object, cache_repo: object):
        self.db_repo = db_repo
        self.cache_repo = cache_repo

    def get(self, code: str) -> CurrencyEntity:
        currency = self.cache_repo.get(code)
        if not currency:
            currency = self.db_repo.get(code)
            self.cache_repo.save(code, currency)
        return currency

    def get_availables(self) -> List[CurrencyEntity]:
        currencies = self.cache_repo.get_availables()
        if not currencies:
            currencies = self.db_repo.get_availables()
            self.cache_repo.save_availables(currencies)
        return currencies

    def save(self, currency: CurrencyEntity):
        self.db_repo.save(currency)

    def bulk_save(self, currencies: List[CurrencyEntity]):
        self.db_repo.bulk_save(currencies)


class CurrencyExchangeRateRepository:

    def __init__(self, db_repo: object, cache_repo: object):
        self.db_repo = db_repo
        self.cache_repo = cache_repo

    def get(self, source_currency: str, exchanged_currency: str,
            valuation_date: str) -> CurrencyExchangeRateEntity:
        exchange_rate = self.cache_repo.get(
            source_currency, exchanged_currency, valuation_date)
        if not exchange_rate:
            exchange_rate = self.db_repo.get(
                source_currency, exchanged_currency, valuation_date)
            self.cache_repo.save(exchange_rate)
        return exchange_rate

    def get_rate_series(self, source_currency: str, exchanged_currency: str,
                        date_from: str, date_to: str) -> List[CurrencyExchangeRateEntity]:
        return self.db_repo.get_rate_series(
            source_currency, exchanged_currency, date_from, date_to)

    def get_time_series(self, source_currency: str, exchanged_currency: str,
                        date_from: str, date_to: str) -> List[CurrencyExchangeRateEntity]:
        return self.db_repo.get_time_series(
            source_currency, exchanged_currency, date_from, date_to)

    def save(self, exchange_rate: CurrencyExchangeRateEntity):
        self.db_repo.save(exchange_rate)

    def bulk_save(self, exchange_rates: List[CurrencyExchangeRateEntity]):
        self.db_repo.bulk_save(exchange_rates)
