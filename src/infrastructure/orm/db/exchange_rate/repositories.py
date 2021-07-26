# coding: utf-8

from typing import List

from django.db.models import Q

from src.domain.exchange_rate import CurrencyEntity, CurrencyExchangeRateEntity
from src.infrastructure.orm.db.exceptions import EntityDoesNotExist
from src.infrastructure.orm.db.exchange_rate.models import (
    Currency, CurrencyExchangeRate)


class CurrencyDatabaseRepository:

    def get(self, code: str) -> CurrencyEntity:
        try:
            currency = Currency.objects.get(code=code).values()
        except Currency.DoesNotExist:
            raise EntityDoesNotExist(
                f'Currency with code {code} does not exist')
        return CurrencyEntity(**currency)

    def get_availables(self) -> List[CurrencyEntity]:
        return list(map(CurrencyEntity, Currency.objects.values()))


class CurrencyExchangeRateDatabaseRepository:

    def get(self, source_currency: str, exchanged_currency: str,
            valuation_date: str) -> CurrencyExchangeRateEntity:
        try:
            exchange_rate = CurrencyExchangeRate.objects.get(
                source_currency=source_currency,
                exchanged_currency=exchanged_currency,
                valuation_date=valuation_date
            ).values()
        except CurrencyExchangeRate.DoesNotExist:
            raise EntityDoesNotExist(
                f'Exchange rate for {source_currency}/{exchanged_currency} '
                f'for {valuation_date} does not exist')
        return CurrencyExchangeRateEntity(**exchange_rate)

    def get_time_series(self, source_currency: str, exchanged_currency: str,
            date_from: str, date_to: str) -> List[CurrencyExchangeRateEntity]:
        qs = Q(source_currency=source_currency) \
             & Q(valuation_date__range=[date_from, date_to])
        if exchanged_currency:
            qs &= Q(exchanged_currency=exchanged_currency)
        time_series = CurrencyExchangeRate.objects.filter(qs).values()
        return list(map(CurrencyExchangeRateEntity, time_series))