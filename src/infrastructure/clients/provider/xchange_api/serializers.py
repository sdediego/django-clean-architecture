# coding: utf-8

from datetime import date

from marshmallow import Schema, fields, EXCLUDE
from marshmallow.decorators import post_load, pre_load


class ExchangeRateSerializer(Schema):

    class Meta:
        unknown = EXCLUDE

    source_currency = fields.String(data_key='base', required=True)
    valuation_date = fields.Date(required=True)
    rates = fields.Dict(
        keys=fields.String(), values=fields.Float(), required=True)

    @pre_load
    def process_date(self, in_data: dict, **kwargs) -> dict:
        timestamp = in_data.pop('timestamp')
        in_data['valuation_date'] = date.fromtimestamp(
            timestamp).strftime('%Y-%m-%d')
        return in_data

    @post_load(pass_original=True)
    def process_rates(self, data: dict, original_data: dict, **kwargs) -> list:
        exchanged_currencies = original_data.get('symbols').split(',')
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
