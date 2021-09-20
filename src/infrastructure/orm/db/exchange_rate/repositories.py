# coding: utf-8

import dataclasses
import json
from typing import List

from src.domain.exchange_rate import CurrencyEntity, CurrencyExchangeRateEntity
from src.infrastructure.orm.db.exchange_rate.models import (
    Currency, CurrencyExchangeRate)
from src.infrastructure.orm.db.exchange_rate.tasks import (
    bulk_save_currencies, bulk_save_exchange_rates, save_currency,
    save_exchange_rate)
from src.interface.repositories.exceptions import EntityDoesNotExist


class CurrencyDatabaseRepository:

    def get(self, code: str) -> CurrencyEntity:
        currency = Currency.objects.filter(code=code).values().first()
        if not currency:
            raise EntityDoesNotExist(f'{code} currency code does not exist')
        return CurrencyEntity(**currency)

    def get_availables(self) -> List[CurrencyEntity]:
        return list(map(lambda x: CurrencyEntity(**x), Currency.objects.values()))

    def save(self, currency: CurrencyEntity):
        currency_json = json.dumps(dataclasses.asdict(currency))
        save_currency.apply_async(kwargs={'currency_json': currency_json})

    def bulk_save(self, currencies: List[CurrencyEntity]):
        currencies_json = json.dumps(list(map(dataclasses.asdict, currencies)))
        bulk_save_currencies.apply_async(kwargs={'currencies_json': currencies_json})


class CurrencyExchangeRateDatabaseRepository:

    def get(self, source_currency: str, exchanged_currency: str,
            valuation_date: str) -> CurrencyExchangeRateEntity:
        exchange_rate = CurrencyExchangeRate.objects.filter(
            source_currency=source_currency,
            exchanged_currency=exchanged_currency,
            valuation_date=valuation_date
        ).values(
            'source_currency', 'exchanged_currency', 'valuation_date', 'rate_value'
        ).first()
        if not exchange_rate:
            raise EntityDoesNotExist(
                f'Exchange rate {source_currency}/{exchanged_currency} '
                f'for {valuation_date} does not exist')
        return CurrencyExchangeRateEntity(**exchange_rate)

    def get_rate_series(self, source_currency: str, exchanged_currency: str,
                        date_from: str, date_to: str) -> List[float]:
        rate_series = CurrencyExchangeRate.objects.filter(
            source_currency=source_currency,
            exchanged_currency=exchanged_currency,
            valuation_date__range=[date_from, date_to]
        ).values_list('rate_value', flat=True)
        return list(map(float, rate_series))

    def get_time_series(self, source_currency: str, exchanged_currency: str,
                        date_from: str, date_to: str) -> List[CurrencyExchangeRateEntity]:
        timeseries = CurrencyExchangeRate.objects.filter(
            source_currency=source_currency,
            exchanged_currency__in=exchanged_currency.split(','),
            valuation_date__range=[date_from, date_to]
        ).values(
            'source_currency', 'exchanged_currency', 'valuation_date', 'rate_value')
        return list(map(lambda x: CurrencyExchangeRateEntity(**x), timeseries))

    def save(self, exchange_rate: CurrencyExchangeRateEntity):
        exchange_rate_json = json.dumps(dataclasses.asdict(exchange_rate))
        save_exchange_rate.apply_async(
            kwargs={'exchange_rate_json': exchange_rate_json})

    def bulk_save(self, exchange_rates: List[CurrencyExchangeRateEntity]):
        exchange_rates_json = json.dumps(
            list(map(dataclasses.asdict, exchange_rates)))
        bulk_save_exchange_rates.apply_async(
            kwargs={'exchange_rates_json': exchange_rates_json})
