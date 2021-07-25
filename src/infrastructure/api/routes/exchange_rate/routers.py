# coding: utf-8

from rest_framework.routers import SimpleRouter, Route

from src.infrastructure.factories.exchange_rates import CurrencyViewsetFactory


class CurrencyRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^$',
            mapping={'get': 'get'},
            name='{basename}-get',
            initkwargs={'view_factory': CurrencyViewsetFactory},
            detail=False
        ),
        Route(
            url=r'^<str:code>/$',
            mapping={'get': 'list'},
            name='{basename}-list',
            initkwargs={'view_factory': CurrencyViewsetFactory},
            detail=True
        )
    ]
