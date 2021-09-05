# coding: utf-8

from marshmallow import Schema, fields
from marshmallow.decorators import post_load


class CurrencySerializer(Schema):
    currencies = fields.List(
        fields.List(), data_key='supported_codes', required=True)

    @post_load
    def make_currencies(self, data: dict, **kwargs) -> dict:
        return [
            {'code': code, 'name': name} for code, name in data['currencies']
        ]


class ExchangeRateSerializer(Schema):
    source_currency = fields.String(data_key='base_code', required=True)
    exchanged_currency = fields.String(required=True)
    year = fields.Integer(strict=True, required=True)
    month = fields.Integer(strict=True, required=True)
    day = fields.Integer(strict=True, required=True)
    rates = fields.Dict(data_key='conversion_rates',
                        keys=fields.String(),
                        values=fields.Float(),
                        required=True)

    @post_load
    def process_exchange_rate(self, data: dict, **kwargs) -> dict:
        valuation_date = f'{data.pop("year")}-{data.pop("month")}-{data.pop("day")}'
        rate_value = data.pop('rates').get(data['exchanged_currency'])
        data['valuation_date'] = valuation_date
        data['rate_value'] = round(float(rate_value), 6)
        return data
