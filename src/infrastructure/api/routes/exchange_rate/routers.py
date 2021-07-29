# coding: utf-8

from rest_framework.routers import SimpleRouter, Route

from src.infrastructure.factories.exchange_rates import (
    CurrencyViewSetFactory, CurrencyExchangeRateViewSetFactory)


class CurrencyRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^$',
            mapping={'get': 'list'},
            name='{basename}-list',
            initkwargs={'viewset_factory': CurrencyViewSetFactory},
            detail=False
        ),
        Route(
            url=r'^(?P<code>[a-zA-Z]+)/$',
            mapping={'get': 'get'},
            name='{basename}-get',
            initkwargs={'viewset_factory': CurrencyViewSetFactory},
            detail=True
        )
    ]


class CurrencyExchangeRateRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^$',
            mapping={'get': 'list'},
            name='{basename}-list',
            initkwargs={'viewset_factory': CurrencyExchangeRateViewSetFactory},
            detail=False
        ),
        Route(
            url=r'^convert/$',
            mapping={'get': 'convert'},
            name='{basename}-convert',
            initkwargs={'viewset_factory': CurrencyExchangeRateViewSetFactory},
            detail=False
        ),
        Route(
            url=r'^time-weighted/$',
            mapping={'get': 'calculate_twr'},
            name='{basename}-calculate-twr',
            initkwargs={'viewset_factory': CurrencyExchangeRateViewSetFactory},
            detail=False
        )
    ]
