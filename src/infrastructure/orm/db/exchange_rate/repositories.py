# coding: utf-8

from django.db.models.query import QuerySet

from src.domain.exchange_rate import CurrencyEntity
from src.infrastructure.orm.db.exceptions import EntityDoesNotExist
from src.infrastructure.orm.db.exchange_rate.models import Currency


class CurrencyDBRepository:

    def _get_currency_entity(self, currency: dict) -> CurrencyEntity:
        currency['rate_value'] = float(currency['rate_value'])
        return CurrencyEntity(**currency)

    def get(self, code: str) -> CurrencyEntity:
        try:
            currency = Currency.objects.get(code=code).values()
        except Currency.DoesNotExist:
            raise EntityDoesNotExist(
                f'Currency with code {code} does not exist')
        return self._get_currency_entity(currency)

    def get_availables(self) -> QuerySet[CurrencyEntity]:
        return Currency.objects.all()
