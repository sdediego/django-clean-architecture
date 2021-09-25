# coding: utf-8

from typing import List

from marshmallow import Schema, fields, EXCLUDE
from marshmallow.decorators import post_load, pre_load

from src.domain.exchange_rate import CurrencyEntity, CurrencyExchangeRateEntity


class CurrencySerializer(Schema):

    class Meta:
        unknown = EXCLUDE

    currencies = fields.Dict(
        data_key='symbols', keys=fields.String(), values=fields.String(), required=True)

    @post_load
    def make_currencies(self, data: dict, **kwargs) -> List[CurrencyEntity]:
        return [
            CurrencyEntity(code=code, name=name)
            for code, name in data.get('currencies').items()
        ]


class ExchangeRateSerializer(Schema):

    class Meta:
        unknown = EXCLUDE

    source_currency = fields.String(data_key='base', required=True)
    exchanged_currency = fields.String(required=True)
    valuation_date = fields.Date(data_key='date', required=True)
    rate_value = fields.Float(required=True)

    @pre_load
    def process_rates(self, in_data: dict, **kwargs) -> dict:
        rates = in_data.pop('rates')
        exchanged_currency, rate_value = tuple(rates.items())[0]
        in_data['exchanged_currency'] = exchanged_currency
        in_data['rate_value'] = round(float(rate_value), 6)
        return in_data

    @post_load
    def make_exchange_rate(self, data: dict, **kwargs) -> CurrencyExchangeRateEntity:
        return CurrencyExchangeRateEntity(**data)


class TimeSeriesSerializer(Schema):

    class Meta:
        unknown = EXCLUDE

    source_currency = fields.String(data_key='base', required=True)
    rates = fields.Dict(
        keys=fields.String(),
        values=fields.Dict(keys=fields.String(), values=fields.Float()),
        required=True)

    @post_load
    def make_exchange_rates(self, data: dict, **kwargs) -> List[CurrencyExchangeRateEntity]:
        source_currency = data.get('source_currency')
        rates = data.get('rates')
        return [
            CurrencyExchangeRateEntity(
                source_currency=source_currency,
                exchanged_currency=exchanged_currency,
                valuation_date=date,
                rate_value=round(float(rate_value), 6)
            )
            for date, exchange_rates in rates.items()
            for exchanged_currency, rate_value in exchange_rates.items()
        ]
