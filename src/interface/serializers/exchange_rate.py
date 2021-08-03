# coding: utf-8

from marshmallow import Schema, fields
from marshmallow.decorators import post_dump, post_load
from marshmallow.exceptions import ValidationError


class CurrencySerializer(Schema):
    code = fields.String(required=True)
    name = fields.String(required=True)
    symbol = fields.String(required=False)


class CurrencyExchangeRateConvertSerializer(Schema):
    source_currency = fields.String(required=True)
    exchanged_currency = fields.String(required=True)
    amount = fields.Float(required=True)

    def load(self, data: dict) -> dict:
        try:
            data = super().load(data)
        except ValidationError as err:
            data = {'errors': err.messages}
        return data

    @post_load
    def make_upper_code(self, data: dict, **kwargs) -> dict:
        data['source_currency'] = data['source_currency'].upper()
        data['exchanged_currency'] = data['exchanged_currency'].upper()
        return data


class CurrencyExchangeRateAmountSerializer(Schema):
    exchanged_currency = fields.String(required=True)
    exchanged_amount = fields.Float(required=True)
    rate_value = fields.Float(required=True)


class CurrencyExchangeRateListSerializer(Schema):
    source_currency = fields.String(required=True)
    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)

    def load(self, data: dict) -> dict:
        try:
            data = super().load(data)
        except ValidationError as err:
            data = {'errors': err.messages}
        return data


class CurrencyExchangeRateSerializer(Schema):
    exchanged_currency = fields.String(required=True)
    valuation_date = fields.String(required=True)
    rate_value = fields.Float(required=True)


class TimeWeightedRateListSerializer(CurrencyExchangeRateListSerializer):
    exchanged_currency = fields.String(required=True)


class TimeWeightedRateSerializer(Schema):
    time_weighted_rate = fields.Float(required=True)

    @post_dump
    def round_float(self, data: dict, **kwargs) -> dict:
        data['time_weighted_rate'] = round(data['time_weighted_rate'], 6)
        return data
