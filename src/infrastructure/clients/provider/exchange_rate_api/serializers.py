# coding: utf-8

from marshmallow import Schema, fields, EXCLUDE
from marshmallow.decorators import post_load


class CurrencySerializer(Schema):

    class Meta:
        unknown = EXCLUDE

    currencies = fields.List(fields.List(fields.String()),
                             data_key='supported_codes',
                             required=True)

    @post_load
    def make_currencies(self, data: dict, **kwargs) -> dict:
        return [
            {'code': code, 'name': name} for code, name in data['currencies']
        ]


class ExchangeRateSerializer(Schema):

    class Meta:
        unknown = EXCLUDE

    source_currency = fields.String(data_key='base_code', required=True)
    year = fields.Integer(strict=True, required=True)
    month = fields.Integer(strict=True, required=True)
    day = fields.Integer(strict=True, required=True)
    rates = fields.Dict(data_key='conversion_rates',
                        keys=fields.String(),
                        values=fields.Float(),
                        required=True)

    @post_load(pass_original=True)
    def process_rates(self, data: dict, original_data: dict, **kwargs) -> list:
        exchanged_currencies = original_data.get('symbols').split(',')
        data['valuation_date'] = (
            f'{data.pop("year")}-{data.pop("month")}-{data.pop("day")}')
        return [
            {
                'source_currency': data.get('source_currency'),
                'exchanged_currency': exchanged_currency,
                'valuation_date': data.get('valuation_date'),
                'rate_value': round(
                    float(data.get('rates').get(exchanged_currency)), 6)
            }
            for exchanged_currency in exchanged_currencies
            if data.get('rates').get(exchanged_currency) is not None
        ]
