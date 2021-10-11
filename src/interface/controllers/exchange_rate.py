# coding: utf-8

import logging
from http import HTTPStatus
from typing import Tuple

from src.domain.exchange_rate import CurrencyExchangeRateEntity
from src.interface.controllers.utils import (
    calculate_time_weighted_rate, calculate_exchanged_amount, filter_currencies,
    get_rate_series)
from src.interface.repositories.exceptions import EntityDoesNotExist
from src.interface.serializers.exchange_rate import (
    CurrencySerializer, CurrencyExchangeRateAmountSerializer,
    CurrencyExchangeRateConvertSerializer, CurrencyExchangeRateListSerializer,
    CurrencyExchangeRateSerializer, TimeWeightedRateListSerializer,
    TimeWeightedRateSerializer)
from src.usecases.exchange_rate import CurrencyInteractor, CurrencyExchangeRateInteractor
from src.usecases.provider import ProviderClientInteractor


logger = logging.getLogger(__name__)


class CurrencyController:

    def __init__(self, currency_interator: CurrencyInteractor,
                 provider_client_interactor: ProviderClientInteractor):
        self.currency_interator = currency_interator
        self.provider_client_interactor = provider_client_interactor

    def get(self, code: str) -> Tuple[dict, int]:
        code = code.upper()
        logger.info('Retrieving %s currency info', code)
        try:
            currency = self.currency_interator.get(code)
        except EntityDoesNotExist as err:
            currency = filter_currencies(
                code, self.provider_client_interactor.fetch_data('currency_get'))
            if currency is None:
                logger.error('Failure retrieving %s currency: %s', code, err.message)
                return {'error': err.message}, HTTPStatus.NOT_FOUND.value
            self.currency_interator.save(currency)
        logger.info('%s currency successfully retrieved', currency.code)
        return CurrencySerializer().dump(currency), HTTPStatus.OK.value

    def list(self) -> Tuple[list, int]:
        logger.info('Retrieving available currencies list')
        currencies = self.currency_interator.get_availables()
        if not currencies:
            currencies = self.provider_client_interactor.fetch_data('currency_list')
            if 'error' in currencies:
                logger.warning('Available currencies list empty')
                currencies = []
            else:
                self.currency_interator.bulk_save(currencies)
        logger.info('Available currencies list succesfully retrieved')
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
        logger.info('Converting currency for params: %s', str(params))
        data = CurrencyExchangeRateConvertSerializer().load(params)
        if 'errors' in data:
            logger.error('Error deserializing params: %s', str(data['errors']))
            return data, HTTPStatus.BAD_REQUEST.value
        amount = data.pop('amount')
        try:
            exchange_rate = self.exchange_rate_interactor.get_latest(**data)
        except EntityDoesNotExist as err:
            exchange_rate = self.provider_client_interactor.fetch_data(
                'exchange_rate_convert', **data)
            if not isinstance(exchange_rate, CurrencyExchangeRateEntity):
                logger.error('Failure converting currency: %s', err.message)
                return {'error': err.message}, HTTPStatus.NOT_FOUND.value
            self.exchange_rate_interactor.save(exchange_rate)
        exchanged_amount = calculate_exchanged_amount(exchange_rate, amount)
        logger.info('Currency successfully converted: %s', str(exchanged_amount))
        return (
            CurrencyExchangeRateAmountSerializer().dump(exchanged_amount),
            HTTPStatus.OK.value
        )

    def list(self, params: dict) -> Tuple[list, int]:
        logger.info('Retrieving currency exchange rate time series: %s', str(params))
        data = CurrencyExchangeRateListSerializer().load(params)
        if 'errors' in data:
            logger.error('Error deserializing params: %s', str(data['errors']))
            return data, HTTPStatus.BAD_REQUEST.value
        timeseries = self.exchange_rate_interactor.get_time_series(**data)
        if not timeseries:
            timeseries = self.provider_client_interactor.fetch_data(
                'exchange_rate_list', **data)
            if 'error' in timeseries:
                logger.warning('Currency exchange rate time series empty')
                timeseries = []
            else:
                self.exchange_rate_interactor.bulk_save(timeseries)
        logger.info('Currency exchange rate time series successfully retrieved')
        return (
            CurrencyExchangeRateSerializer(many=True).dump(timeseries),
            HTTPStatus.OK.value
        )

    def calculate_twr(self, params: dict) -> Tuple[dict, int]:
        logger.info('Calculating time weighted rate for params: %s', str(params))
        data = TimeWeightedRateListSerializer().load(params)
        if 'errors' in data:
            logger.error('Error deserializing params: %s', str(data['errors']))
            return data, HTTPStatus.BAD_REQUEST.value
        rate_series = self.exchange_rate_interactor.get_rate_series(**data)
        if not rate_series:
            timeseries = self.provider_client_interactor.fetch_data(
                'exchange_rate_calculate_twr', **data)
            if 'error' in timeseries:
                logger.error('Error calculating time weighted rate: %s', str(timeseries['error']))
                return {'error': timeseries['error']}, timeseries['status_code']
            self.exchange_rate_interactor.bulk_save(timeseries)
            rate_series = get_rate_series(timeseries)
        time_weighted_rate = calculate_time_weighted_rate(rate_series)
        logger.info('Time weighted rate successfully calculated')
        return (
            TimeWeightedRateSerializer().dump(time_weighted_rate),
            HTTPStatus.OK.value
        )
