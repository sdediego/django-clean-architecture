# coding: utf-8

from marshmallow import Schema, fields
from marshmallow.decorators import post_load, pre_load


class CurrencySerializer(Schema):
    currencies = fields.Dict(
        data_key='symbols', keys=fields.String(), values=fields.String(), required=True)

    @post_load
    def make_currencies(self, data: dict, **kwargs) -> dict:
        return [
            {'code': code, 'name': name} for code, name in data['currencies'].items()
        ]


class ExchangeRateSerializer(Schema):
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


class TimeSeriesSerializer(Schema):
    source_currency = fields.String(data_key='base', required=True)
    rates = fields.Dict(
        keys=fields.String(),
        values=fields.Dict(keys=fields.String(), values=fields.Float()),
        required=True)

    @post_load
    def make_exchange_rates(self, data: dict, **kwargs) -> dict:
        return [
            {
                'source_currency': data['source_currency'],
                'exchanged_currency': exchanged_currency,
                'valuation_date': date,
                'rate_value': round(float(rate), 6)
            }
            for date, rates in data['rates'].items() for exchanged_currency, rate in rates
        ]
