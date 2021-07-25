# coding: utf-8

from src.infrastructure.orm.db.exchange_rate.repositories import CurrencyDatabaseRepository
from src.interface.controllers.exchange_rate import CurrencyController
from src.interface.repositories.exchange_rate import CurrencyRepository
from src.usecases.exchange_rate import CurrencyInteractor


class CurrencyDatabaseRepositoryFactory:

    @staticmethod
    def get():
        return CurrencyDatabaseRepository()


class CurrencyRepositoryFactory:

    @staticmethod
    def get():
        db_repo = CurrencyDatabaseRepositoryFactory.get()
        return CurrencyRepository(db_repo)


class CurrencyInteractorFactory:

    @staticmethod
    def get():
        currency_repo = CurrencyRepositoryFactory.get()
        return CurrencyInteractor(currency_repo)


class CurrencyViewsetFactory:

    @staticmethod
    def create():
        currency_interactor = CurrencyInteractorFactory.get()
        return CurrencyController(currency_interactor)
