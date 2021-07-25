# coding: utf-8

from marshmallow import Schema, fields


class CurrencySerializer(Schema):
    code = fields.String(required=True)
    name = fields.String(required=True)
    symbol = fields.String(required=True)
