# coding: utf-8

from src.infrastructure.factories.provider import ProviderClientInteractorFactory
from src.infrastructure.orm.cache.exchange_rate.repositories import (
    CurrencyCacheRepository, CurrencyExchangeRateCacheRepository)
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
    def get() -> CurrencyDatabaseRepository:
        return CurrencyDatabaseRepository()


class CurrencyCacheRepositoryFactory:

    @staticmethod
    def get() -> CurrencyCacheRepository:
        return CurrencyCacheRepository()


class CurrencyRepositoryFactory:

    @staticmethod
    def get() -> CurrencyRepository:
        db_repo = CurrencyDatabaseRepositoryFactory.get()
        cache_repo = CurrencyCacheRepositoryFactory.get()
        return CurrencyRepository(db_repo, cache_repo)


class CurrencyInteractorFactory:

    @staticmethod
    def get() -> CurrencyInteractor:
        currency_repo = CurrencyRepositoryFactory.get()
        return CurrencyInteractor(currency_repo)


class CurrencyViewSetFactory:

    @staticmethod
    def create() -> CurrencyController:
        currency_interactor = CurrencyInteractorFactory.get()
        provider_client_interactor = ProviderClientInteractorFactory.get()
        return CurrencyController(
            currency_interactor,
            provider_client_interactor
        )


class CurrencyExchangeRateDatabaseRepositoryFactory:

    @staticmethod
    def get() -> CurrencyExchangeRateDatabaseRepository:
        return CurrencyExchangeRateDatabaseRepository()


class CurrencyExchangeRateCacheRepositoryFactory:

    @staticmethod
    def get() -> CurrencyExchangeRateCacheRepository:
        return CurrencyExchangeRateCacheRepository()


class CurrencyExchangeRateRepositoryFactory:

    @staticmethod
    def get() -> CurrencyExchangeRateRepository:
        db_repo = CurrencyExchangeRateDatabaseRepositoryFactory.get()
        cache_repo = CurrencyExchangeRateCacheRepositoryFactory.get()
        return CurrencyExchangeRateRepository(db_repo, cache_repo)


class CurrencyExchangeRateInteractorFactory:

    @staticmethod
    def get() -> CurrencyExchangeRateInteractor:
        exchange_rate_repo = CurrencyExchangeRateRepositoryFactory.get()
        return CurrencyExchangeRateInteractor(exchange_rate_repo)


class CurrencyExchangeRateViewSetFactory:

    @staticmethod
    def create() -> CurrencyExchangeRateController:
        exchange_rate_interactor = CurrencyExchangeRateInteractorFactory.get()
        provider_client_interactor = ProviderClientInteractorFactory.get()
        return CurrencyExchangeRateController(
            exchange_rate_interactor,
            provider_client_interactor
        )
