# coding: utf-8

import json

from celery import shared_task

from src.infrastructure.orm.db.exchange_rate.models import (
    Currency, CurrencyExchangeRate)


def get_currency(code: str, name: str = None) -> Currency:
    attrs = {'code': code}
    try:
        currency = Currency.objects.get(**attrs)
    except Currency.DoesNotExist:
        if name is not None:
            attrs.update({'name': name})
        currency = Currency.objects.create(**attrs)
    return currency


@shared_task
def save_currency(currency_json: str):
    currency = json.loads(currency_json)
    Currency.objects.create(
        code=currency.get('code'),
        name=currency.get('name'),
        symbol=currency.get('symbol')
    )


@shared_task
def save_exchange_rate(exchange_rate_json: str):
    exchange_rate = json.loads(exchange_rate_json)
    source_currency = get_currency(exchange_rate.get('source_currency'))
    exchanged_currency = get_currency(exchange_rate.get('exchanged_currency'))

    CurrencyExchangeRate.objects.create(
        source_currency=source_currency,
        exchanged_currency=exchanged_currency,
        valuation_date=exchange_rate.get('valuation_date'),
        rate_value=exchange_rate.get('rate_value')
    )


@shared_task
def bulk_save_currencies(currencies_json: str):
    currencies = json.loads(currencies_json)
    batch = [
        Currency(
            code=currency.get('code'),
            name=currency.get('name'),
            symbol=currency.get('symbol')
        )
        for currency in currencies
    ]
    Currency.objects.bulk_create(batch, ignore_conflicts=True)


@shared_task
def bulk_save_exchange_rates(exchange_rates_json: str):
    exchange_rates = json.loads(exchange_rates_json)
    source_currency = get_currency(exchange_rates[0].get('source_currency'))
    exchanged_codes = set(list(
        map(lambda x: x.get('exchanged_currency'), exchange_rates)))
    exchanged_currencies = {
        code: get_currency(code) for code in list(exchanged_codes)
    }

    batch = [
        CurrencyExchangeRate(
            source_currency=source_currency,
            exchanged_currency=exchanged_currencies.get(
                exchange_rate.get('exchanged_currency')),
            valuation_date=exchange_rate.get('valuation_date'),
            rate_value=exchange_rate.get('rate_value')
        )
        for exchange_rate in exchange_rates
    ]
    CurrencyExchangeRate.objects.bulk_create(batch, ignore_conflicts=True)
