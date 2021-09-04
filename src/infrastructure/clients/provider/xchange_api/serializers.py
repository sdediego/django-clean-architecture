# coding: utf-8

from datetime import date

from marshmallow import Schema, fields
from marshmallow.decorators import pre_load


class ExchangeRateSerializer(Schema):
    source_currency = fields.String(data_key='base', required=True)
    exchanged_currency = fields.String(required=True)
    valuation_date = fields.Date(required=True)
    rate_value = fields.Float(required=True)

    @pre_load
    def process_rates(self, in_data: dict, **kwargs) -> dict:
        timestamp = in_data.pop('timestamp')
        rates = in_data.pop('rates')
        exchanged_currency, rate_value = tuple(rates.items())[0]
        in_data['valuation_date'] = date.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        in_data['exchanged_currency'] = exchanged_currency
        in_data['rate_value'] = round(float(rate_value), 6)
        return in_data
