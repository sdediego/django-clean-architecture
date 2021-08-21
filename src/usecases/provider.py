# coding: utf-8

import datetime
from typing import List

from src.domain.exchange_rate import (
    CurrencyExchangeRateEntity, CurrencyExchangeAmountEntity)
from src.domain.provider import ProviderEntity


class ProviderInteractor:

    def __init__(self, provider_repo: object):
        self.provider_repo = provider_repo

    def get_by_priority(self) -> List[ProviderEntity]:
        return self.provider_repo.get_by_priority()


class ProviderClientInteractor:

    def __init__(self, provider_driver: object):
        self.provider_driver = provider_driver

    def convert_currency_amount(self, source_currency: str, exchanged_currency: str,
                                amount: float) -> CurrencyExchangeAmountEntity:
        return self.provider_driver.convert_currency_amount(
            source_currency, exchanged_currency, amount)

    def get_exchange_rate(self, source_currency: str, exchanged_currency: str,
                          date: str) -> CurrencyExchangeRateEntity:
        return self.provider_driver.get_exchange_rate(
            source_currency, exchanged_currency, date)

    def get_latest_exchange_rate(self, source_currency: str,
                                 exchanged_currency: str) -> CurrencyExchangeRateEntity:
        today = datetime.date.today().strftime('%Y-%m-%d')
        return self.get_exchange_rate(source_currency, exchanged_currency, today)

    def get_time_series(self, source_currency: str, exchanged_currency: str,
                        date_from: str, date_to: str) -> List[CurrencyExchangeRateEntity]:
        return self.provider_driver.get_time_series(
            source_currency, exchanged_currency, date_from, date_to)

    def get_many_time_series(self, source_currency: str, exchanged_currencies: str,
                             date_from: str, date_to: str) -> List[CurrencyExchangeRateEntity]:
        return self.provider_driver.get_many_time_series(
            source_currency, exchanged_currencies, date_from, date_to)

    def get_rate_series(self, source_currency: str, exchanged_currency: str,
                        date_from: str, date_to: str) -> List[float]:
        time_series = self.get_time_series(source_currency, exchanged_currency,
                                           date_from, date_to)
        return list(map(lambda exchange_rate: exchange_rate.rate_value, time_series))
