# coding: utf-8

from http import HTTPStatus
from typing import Tuple

from src.infrastructure.orm.db.exceptions import EntityDoesNotExist
from src.interface.serializers.exchange_rate import CurrencySerializer


class CurrencyController:

    def __init__(self, currency_iterator: object):
        self.currency_iterator = currency_iterator

    def get(self, code: str) -> Tuple[dict, int]:
        try:
            currency = self.currency_iterator.get(code)
        except EntityDoesNotExist as err:
            return {'error': err.message}, HTTPStatus.NOT_FOUND.value
        return CurrencySerializer().dump(currency), HTTPStatus.OK.value

    def list(self) -> Tuple[list, int]:
        currencies = self.currency_iterator.get_availables()
        return (
            CurrencySerializer(many=True).dump(currencies),
            HTTPStatus.OK.value
        )
