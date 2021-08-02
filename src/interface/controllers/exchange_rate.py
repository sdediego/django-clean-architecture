# coding: utf-8

from http import HTTPStatus
from typing import Tuple

from src.domain.exchange_rate import (
    CurrencyExchangeAmountEntity, TimeWeightedRateEntity)
from src.interface.controllers.utils import calculate_time_weighted_rate
from src.interface.repositories.exceptions import EntityDoesNotExist
from src.interface.serializers.exchange_rate import (
    CurrencySerializer, CurrencyExchangeRateAmountSerializer,
    CurrencyExchangeRateConvertSerializer, CurrencyExchangeRateListSerializer,
    CurrencyExchangeRateSerializer, TimeWeightedRateListSerializer,
    TimeWeightedRateSerializer)


class CurrencyController:

    def __init__(self, currency_interator: object):
        self.currency_interator = currency_interator

    def get(self, code: str) -> Tuple[dict, int]:
        try:
            currency = self.currency_interator.get(code.upper())
        except EntityDoesNotExist as err:
            return {'error': err.message}, HTTPStatus.NOT_FOUND.value
        return CurrencySerializer().dump(currency), HTTPStatus.OK.value

    def list(self) -> Tuple[list, int]:
        currencies = self.currency_interator.get_availables()
        return (
            CurrencySerializer(many=True).dump(currencies),
            HTTPStatus.OK.value
        )


class CurrencyExchangeRateController:

    def __init__(self, exchange_rate_interactor: object):
        self.exchange_rate_interactor = exchange_rate_interactor

    def convert(self, params: dict) -> Tuple[dict, int]:
        data = CurrencyExchangeRateConvertSerializer().load(params)
        if 'errors' in data:
            return data, HTTPStatus.BAD_REQUEST.value
        amount = data.pop('amount')
        try:
            exchange_rate = self.exchange_rate_interactor.get_latest(**data)
        except EntityDoesNotExist as err:
            return {'error': err.message}, HTTPStatus.NOT_FOUND.value
        exchanged_amount = CurrencyExchangeAmountEntity(
            exchanged_currency=data.get('exchanged_currency'),
            exchanged_amount=exchange_rate.calculate_amount(amount),
            rate_value=exchange_rate.rate_value
        )
        return (
            CurrencyExchangeRateAmountSerializer().dump(exchanged_amount),
            HTTPStatus.OK.value
        )

    def list(self, params: dict) -> Tuple[list, int]:
        data = CurrencyExchangeRateListSerializer().load(params)
        if 'errors' in data:
            return data, HTTPStatus.BAD_REQUEST.value
        time_series = self.exchange_rate_interactor.get_all_time_series(**data)
        return (
            CurrencyExchangeRateSerializer(many=True).dump(time_series),
            HTTPStatus.OK.value
        )

    def calculate_twr(self, params: dict) -> Tuple[dict, int]:
        data = TimeWeightedRateListSerializer().load(params)
        if 'errors' in data:
            return data, HTTPStatus.BAD_REQUEST.value
        rate_series = self.exchange_rate_interactor.get_rate_series(**data)
        time_weighted_rate = TimeWeightedRateEntity(
            time_weighted_rate=calculate_time_weighted_rate(rate_series)
        )
        return (
            TimeWeightedRateSerializer().dump(time_weighted_rate),
            HTTPStatus.OK.value
        )
