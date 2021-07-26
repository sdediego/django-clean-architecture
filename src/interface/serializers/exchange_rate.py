# coding: utf-8

from marshmallow import Schema, fields
from marshmallow.decorators import post_dump
from marshmallow.exceptions import ValidationError


class CurrencySerializer(Schema):
    code = fields.String(required=True)
    name = fields.String(required=True)
    symbol = fields.String(required=True)


class CurrencyExchangeRateBase(Schema):

    def load(self, data: dict) -> dict:
        try:
            data = super().load(data)
        except ValidationError as err:
            data = {'errors': err.messages}
        return data


class CurrencyExchangeRateConvertSerializer(CurrencyExchangeRateBase):
    source_currency = fields.String(required=True)
    exchanged_currency = fields.String(required=True)
    amount = fields.Float(required=True)


class CurrencyExchangeRateAmountSerializer(Schema):
    exchanged_currency: str
    exchanged_amount: float
    rate_value: float


class CurrencyExchangeRateListSerializer(CurrencyExchangeRateBase):
    source_currency = fields.String(required=True)
    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)


class CurrencyExchangeRateSerializer(Schema):
    source_currency = fields.String(required=False)
    exchanged_curreyncy = fields.String(required=True)
    valuation_date = fields.Date(required=True)
    rate_value = fields.Decimal(required=True)

    @post_dump(pass_many=True)
    def convert_rate_value_to_float(self, data: dict, many: bool) -> dict:
        data['rate_Value'] = float(data['rate_value'])
        return data


class TimeWeightedRateSerializer(Schema):
    time_weighted_rate: float

    @post_dump
    def round_float(self, data: dict) -> dict:
        data['time_weighted_rate'] = round(data['time_weighted_rate'], 6)
        return data
