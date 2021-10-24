# coding: utf-8

from src.domain.core.constants import HTTP_VERB_GET
from src.domain.core.routing import Route, Router
from src.interface.controllers.exchange_rate import (
    CurrencyController, CurrencyExchangeRateController)
from src.interface.routes.constants import (
    CURRENCIES_PREFIX, EXCHANGE_RATE_PREFIX)


currency_router = Router()
currency_router.register([
    Route(
        http_verb=HTTP_VERB_GET,
        path=fr'^{EXCHANGE_RATE_PREFIX}/{CURRENCIES_PREFIX}/(?P<code>[a-zA-Z]+)/$',
        controller=CurrencyController,
        method='get',
        name='currencies_get',
    ),
    Route(
        http_verb=HTTP_VERB_GET,
        path=fr'^{EXCHANGE_RATE_PREFIX}/{CURRENCIES_PREFIX}/$',
        controller=CurrencyController,
        method='list',
        name='currencies_list',
    ),
])


exchange_rate_router = Router()
exchange_rate_router.register([
    Route(
        http_verb=HTTP_VERB_GET,
        path=fr'^{EXCHANGE_RATE_PREFIX}/time-weighted/$',
        controller=CurrencyExchangeRateController,
        method='calculate_twr',
        name='exchange_rate_calculate_twr',
    ),
    Route(
        http_verb=HTTP_VERB_GET,
        path=fr'^{EXCHANGE_RATE_PREFIX}/convert/$',
        controller=CurrencyExchangeRateController,
        method='convert',
        name='exchange_rate_convert',
    ),
    Route(
        http_verb=HTTP_VERB_GET,
        path=fr'^{EXCHANGE_RATE_PREFIX}/$',
        controller=CurrencyExchangeRateController,
        method='list',
        name='exchange_rate_list',
    ),
])
