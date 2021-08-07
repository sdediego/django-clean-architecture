# coding: utf-8

from src.infrastructure.orm.cache.exchange_rate.repositories import (
    CurrencyCacheRepository)
from src.infrastructure.orm.db.exchange_rate.repositories import (
    CurrencyDatabaseRepository, CurrencyExchangeRateDatabaseRepository)
from src.interface.controllers.exchange_rate import (
    CurrencyController, CurrencyExchangeRateController)
from src.interface.repositories.exchange_rate import (
    CurrencyRepository, CurrencyExchangeRateRepository)
from src.usecases.exchange_rate import (
    CurrencyInteractor, CurrencyExchangeRateInteractor)


class CurrencyDatabaseRepositoryFactory:

    @staticmethod
    def get():
        return CurrencyDatabaseRepository()


class CurrencyCacheRepositoryFactory:

    @staticmethod
    def get():
        return CurrencyCacheRepository()


class CurrencyRepositoryFactory:

    @staticmethod
    def get():
        db_repo = CurrencyDatabaseRepositoryFactory.get()
        cache_repo = CurrencyCacheRepositoryFactory.get()
        return CurrencyRepository(db_repo, cache_repo)


class CurrencyInteractorFactory:

    @staticmethod
    def get():
        currency_repo = CurrencyRepositoryFactory.get()
        return CurrencyInteractor(currency_repo)


class CurrencyViewSetFactory:

    @staticmethod
    def create():
        currency_interactor = CurrencyInteractorFactory.get()
        return CurrencyController(currency_interactor)


class CurrencyExchangeRateDatabaseRepositoryFactory:

    @staticmethod
    def get():
        return CurrencyExchangeRateDatabaseRepository()


class CurrencyExchangeRateRepositoryFactory:

    @staticmethod
    def get():
        db_repo = CurrencyExchangeRateDatabaseRepositoryFactory.get()
        return CurrencyExchangeRateRepository(db_repo)


class CurrencyExchangeRateInteractorFactory:

    @staticmethod
    def get():
        exchange_rate_repo = CurrencyExchangeRateRepositoryFactory.get()
        return CurrencyExchangeRateInteractor(exchange_rate_repo)


class CurrencyExchangeRateViewSetFactory:

    @staticmethod
    def create():
        exchange_rate_interactor = CurrencyExchangeRateInteractorFactory.get()
        return CurrencyExchangeRateController(exchange_rate_interactor)
