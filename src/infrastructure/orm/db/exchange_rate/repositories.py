# coding: utf-8

from typing import List

from django.db.models import Q

from src.domain.exchange_rate import CurrencyEntity, CurrencyExchangeRateEntity
from src.infrastructure.orm.db.exchange_rate.models import (
    Currency, CurrencyExchangeRate)
from src.interface.repositories.exceptions import EntityDoesNotExist


class CurrencyDatabaseRepository:

    def get(self, code: str) -> CurrencyEntity:
        currency = Currency.objects.filter(code=code).values().first()
        if not currency:
            raise EntityDoesNotExist(f'{code} currency code does not exist')
        return CurrencyEntity(**currency)

    def get_availables(self) -> List[CurrencyEntity]:
        return list(map(lambda x: CurrencyEntity(**x), Currency.objects.values()))


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
        qs = Q(source_currency=source_currency) & Q(
            valuation_date__range=[date_from, date_to])
        if exchanged_currency:
            qs &= Q(exchanged_currency=exchanged_currency)
        time_series = CurrencyExchangeRate.objects.filter(qs).values(
            'source_currency', 'exchanged_currency', 'valuation_date', 'rate_value')
        return list(map(lambda x: CurrencyExchangeRateEntity(**x), time_series))
