# coding: utf-8

from src.infrastructure.clients.provider.drivers import ProviderMasterDriver
from src.infrastructure.orm.cache.provider.repositores import ProviderCacheRepository
from src.infrastructure.orm.db.provider.repositories import ProviderDatabaseRepository
from src.interface.clients.provider import ProviderClient
from src.interface.repositories.provider import ProviderRepository
from src.usecases.provider import ProviderInteractor


class ProviderDatabaseRepositoryFactory:

    @staticmethod
    def get():
        return ProviderDatabaseRepository()


class ProviderCacheRepositoryFactory:

    @staticmethod
    def get():
        return ProviderCacheRepository()


class ProviderRepositoryFactory:

    @staticmethod
    def get():
        db_repo = ProviderDatabaseRepositoryFactory.get()
        cache_repo = ProviderCacheRepositoryFactory.get()
        return ProviderRepository(db_repo, cache_repo)


class ProviderInteractorFactory:

    @staticmethod
    def get():
        provider_repo = ProviderRepositoryFactory.get()
        return ProviderInteractor(provider_repo)


class ProviderDriverFactory:

    @staticmethod
    def get():
        provider_interactor = ProviderInteractorFactory.get()
        return ProviderMasterDriver(provider_interactor)


class ProviderClientFactory:

    @staticmethod
    def get():
        provider_driver = ProviderDriverFactory.get()
        return ProviderClient(provider_driver)
