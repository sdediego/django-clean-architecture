# coding: utf-8

from rest_framework.routers import SimpleRouter, Route

from src.infrastructure.factories.exchange_rates import (
    CurrencyViewSetFactory, CurrencyExchangeRateViewSetFactory)
from src.interface.routes.exchange_rate import (
   currency_router, exchange_rate_router)


class CurrencyRouter(SimpleRouter):
    routes = [
         Route(
            url=currency_router.get_url('currencies_list'),
            mapping=currency_router.map('currencies_list'),
            initkwargs={'viewset_factory': CurrencyViewSetFactory},
            name='{basename}-list',
            detail=False,
        ),
        Route(
            url=currency_router.get_url('currencies_get'),
            mapping=currency_router.map('currencies_get'),
            initkwargs={'viewset_factory': CurrencyViewSetFactory},
            name='{basename}-get',
            detail=False,
        ),
    ]


class CurrencyExchangeRateRouter(SimpleRouter):
    routes = [
        Route(
            url=exchange_rate_router.get_url('exchange_rate_list'),
            mapping=exchange_rate_router.map('exchange_rate_list'),
            initkwargs={'viewset_factory': CurrencyExchangeRateViewSetFactory},
            name='{basename}-list',
            detail=False,
        ),
        Route(
            url=exchange_rate_router.get_url('exchange_rate_convert'),
            mapping=exchange_rate_router.map('exchange_rate_convert'),
            initkwargs={'viewset_factory': CurrencyExchangeRateViewSetFactory},
            name='{basename}-convert',
            detail=False,
        ),
        Route(
            url=exchange_rate_router.get_url('exchange_rate_calculate_twr'),
            mapping=exchange_rate_router.map('exchange_rate_calculate_twr'),
            initkwargs={'viewset_factory': CurrencyExchangeRateViewSetFactory},
            name='{basename}-calculate-twr',
            detail=False,
        ),
    ]
