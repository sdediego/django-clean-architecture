# coding: utf-8

import time
from typing import List

from src.domain.exchange_rate import CurrencyEntity, CurrencyExchangeRateEntity
from src.infrastructure.clients.provider.mock import requests
from src.infrastructure.clients.provider.utils import get_last_business_day


class MockDriver:
    SLEEP_TIME = 2
    CURRENCIES = 'currencies'
    HISTORICAL_RATE = 'historical'
    TIME_SERIES = 'timeseries'
    ACTION_MAP = {
        CURRENCIES: requests.currencies,
        HISTORICAL_RATE: requests.historical_rate,
        TIME_SERIES: requests.timeseries_rates,
    }

    def _request(self, endpoint: str, data: dict = None) -> dict:
        time.sleep(self.SLEEP_TIME)
        request = self.ACTION_MAP.get(endpoint)
        return request(data)

    def get_currencies(self) -> List[CurrencyEntity]:
        return self._request(self.CURRENCIES)

    def get_exchange_rate(self, source_currency: str, exchanged_currency: str,
                          date: str = None) -> CurrencyExchangeRateEntity:
        data = {
            'source_currency': source_currency,
            'exchanged_currency': exchanged_currency,
            'valuation_date': date or get_last_business_day(),
        }
        return self._request(self.HISTORICAL_RATE, data)

    def get_time_series(self, source_currency: str, exchanged_currency: str,
                        date_from: str, date_to: str) -> List[CurrencyExchangeRateEntity]:
        data = {
            'source_currency': source_currency,
            'exchanged_currency': exchanged_currency,
            'date_from': date_from,
            'date_to': date_to,
        }
        return self._request(self.TIME_SERIES, data)
