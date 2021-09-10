# coding: utf-8

from src.infrastructure.orm.cache.provider.repositores import ProviderCacheRepository
from src.infrastructure.orm.db.provider.repositories import ProviderDatabaseRepository
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
