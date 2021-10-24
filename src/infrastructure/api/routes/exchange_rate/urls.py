# coding: utf-8

from django.conf.urls import include
from django.urls import path

from src.infrastructure.api.routes.exchange_rate.routers import (
    CurrencyRouter, CurrencyExchangeRateRouter)
from src.infrastructure.api.views.exchange_rate import (
    CurrencyViewSet, CurrencyExchangeRateViewSet)


currency_router = CurrencyRouter()
currency_router.register('', viewset=CurrencyViewSet, basename='currencies')


exchange_rate_router = CurrencyExchangeRateRouter()
exchange_rate_router.register(
    '', viewset=CurrencyExchangeRateViewSet, basename='exchange-rate')


urlpatterns = [
    path('', include(exchange_rate_router.urls)),
    path('', include(currency_router.urls))
]
