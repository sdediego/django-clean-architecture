# coding: utf-8

from http import HTTPStatus
from typing import Tuple

from src.domain.exchange_rate import (
    CurrencyExchangeAmountEntity, CurrencyExchangeRateEntity, TimeWeightedRateEntity)
from src.interface.controllers.utils import (
    calculate_time_weighted_rate, filter_currencies, get_rate_series)
from src.interface.repositories.exceptions import EntityDoesNotExist
from src.interface.serializers.exchange_rate import (
    CurrencySerializer, CurrencyExchangeRateAmountSerializer,
    CurrencyExchangeRateConvertSerializer, CurrencyExchangeRateListSerializer,
    CurrencyExchangeRateSerializer, TimeWeightedRateListSerializer,
    TimeWeightedRateSerializer)
from src.usecases.exchange_rate import CurrencyInteractor, CurrencyExchangeRateInteractor
from src.usecases.provider import ProviderClientInteractor


class CurrencyController:

    def __init__(self, currency_interator: CurrencyInteractor,
                 provider_client_interactor: ProviderClientInteractor):
        self.currency_interator = currency_interator
        self.provider_client_interactor = provider_client_interactor

    def get(self, code: str) -> Tuple[dict, int]:
        try:
            currency = self.currency_interator.get(code.upper())
        except EntityDoesNotExist as err:
            currency = filter_currencies(
                code.upper(), self.provider_client_interactor.fetch_data('currency_get'))
            if currency is None:
                return {'error': err.message}, HTTPStatus.NOT_FOUND.value
            self.currency_interator.save(currency)
        return CurrencySerializer().dump(currency), HTTPStatus.OK.value

    def list(self) -> Tuple[list, int]:
        currencies = self.currency_interator.get_availables()
        if not currencies:
            currencies = self.provider_client_interactor.fetch_data('currency_list')
            if 'error' in currencies:
                currencies = []
            else:
                self.currency_interator.bulk_save(currencies)
        return (
            CurrencySerializer(many=True).dump(currencies),
            HTTPStatus.OK.value
        )


class CurrencyExchangeRateController:

    def __init__(self, exchange_rate_interactor: CurrencyExchangeRateInteractor,
                 provider_client_interactor: ProviderClientInteractor):
        self.exchange_rate_interactor = exchange_rate_interactor
        self.provider_client_interactor = provider_client_interactor

    def convert(self, params: dict) -> Tuple[dict, int]:
        data = CurrencyExchangeRateConvertSerializer().load(params)
        if 'errors' in data:
            return data, HTTPStatus.BAD_REQUEST.value
        amount = data.pop('amount')
        try:
            exchange_rate = self.exchange_rate_interactor.get_latest(**data)
        except EntityDoesNotExist as err:
            exchange_rate = self.provider_client_interactor.fetch_data(
                'exchange_rate_convert', **data)
            if not isinstance(exchange_rate, CurrencyExchangeRateEntity):
                return {'error': err.message}, HTTPStatus.NOT_FOUND.value
            self.exchange_rate_interactor.save(exchange_rate)
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
        timeseries = self.exchange_rate_interactor.get_time_series(**data)
        if not timeseries:
            timeseries = self.provider_client_interactor.fetch_data(
                'exchange_rate_list', **data)
            if 'error' in timeseries:
                timeseries = []
            else:
                self.exchange_rate_interactor.bulk_save(timeseries)
        return (
            CurrencyExchangeRateSerializer(many=True).dump(timeseries),
            HTTPStatus.OK.value
        )

    def calculate_twr(self, params: dict) -> Tuple[dict, int]:
        data = TimeWeightedRateListSerializer().load(params)
        if 'errors' in data:
            return data, HTTPStatus.BAD_REQUEST.value
        rate_series = self.exchange_rate_interactor.get_rate_series(**data)
        if not rate_series:
            timeseries = self.provider_client_interactor.fetch_data(
                'exchange_rate_calculate_twr', **data)
            if 'error' in timeseries:
                return {'error': timeseries['error']}, timeseries['status_code']
            self.exchange_rate_interactor.bulk_save(timeseries)
            rate_series = get_rate_series(timeseries)
        time_weighted_rate = TimeWeightedRateEntity(
            time_weighted_rate=calculate_time_weighted_rate(rate_series)
        )
        return (
            TimeWeightedRateSerializer().dump(time_weighted_rate),
            HTTPStatus.OK.value
        )
