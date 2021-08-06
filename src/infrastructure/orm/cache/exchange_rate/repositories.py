# coding: utf-8

from typing import List, Union

from django.core.cache import cache

from src.domain.exchange_rate import CurrencyEntity, CurrencyExchangeRateEntity
from src.infrastructure.orm.cache.exchange_rate.constants import (
    CACHE_AVAILABLE_CURRENCIES_KEY, CACHE_EXCHANGE_RATE_KEY)


class CurrencyCacheRepository:

    def get(self, key: str) -> CurrencyEntity:
        return cache.get(key)

    def get_availables(self) -> List[CurrencyEntity]:
        return self.get(CACHE_AVAILABLE_CURRENCIES_KEY)

    def save(self, key: str, value: Union[CurrencyEntity, list]):
        cache.set(key, value)

    def save_availables(self, currencies: List[CurrencyEntity]):
        self.save(CACHE_AVAILABLE_CURRENCIES_KEY, currencies)


class CurrencyExchangeRateCacheRepository:

    @staticmethod
    def get_exchange_rate_key(source_currency: str, exchanged_currency: str,
                              valuation_date: str) -> str:
        return CACHE_EXCHANGE_RATE_KEY.format(
            source_currency=source_currency,
            exchanged_currency=exchanged_currency,
            valuation_date=valuation_date
        )

    def get(self, source_currency: str, exchanged_currency: str,
            valuation_date: str) -> CurrencyExchangeRateEntity:
        key = self.get_exchange_rate_key(
            source_currency, exchanged_currency, valuation_date)
        return cache.get(key)

    def save(self, exchange_rate: CurrencyExchangeRateEntity):
        key = self.get_exchange_rate_key(
            exchange_rate.source_currency,
            exchange_rate.exchanged_currency,
            exchange_rate.valuation_date)
        cache.set(key, exchange_rate)
