# coding: utf-8

import json
import random
from typing import List

from src.domain.exchange_rate import CurrencyEntity, CurrencyExchangeRateEntity
from src.infrastructure.clients.provider.utils import (
    get_business_days, get_last_business_day)


def currencies() -> List[CurrencyEntity]:
    with open('../xchange_api/currencies.json', 'r') as currencies_file:
        data = json.load(currencies_file)
    return [CurrencyEntity(**currency) for currency in data['availableCurrencies']]


def historical_rate(data: dict) -> CurrencyExchangeRateEntity:
    return CurrencyExchangeRateEntity(
        source_currency=data.get('source_currency'),
        exchanged_currency=data.get('exchanged_currency'),
        valuation_date=get_last_business_day(data.get('valuation_date')),
        rate_value=round(random.uniform(0.5, 1.5), 6)
    )


def timeseries_rates(data: dict) -> List[CurrencyExchangeRateEntity]:
    source_currency = data.get('source_currency')
    exchanged_currencies = data.get('exchanged_currency').split(',')
    business_days = get_business_days(data.get('date_from'), data.get('date_to'))
    return [
        CurrencyExchangeRateEntity(
            source_currency=source_currency,
            exchanged_currency=currency,
            valuation_date=business_day,
            rate_value=round(random.uniform(0.5, 1.5), 6)
        )
        for business_day in business_days for currency in exchanged_currencies
    ]
