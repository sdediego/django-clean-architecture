# coding: utf-8

from django.conf.urls import include
from django.urls import path

from src.infrastructure.api.routes.exchange_rate.routers import CurrencyRouter
from src.infrastructure.api.views.exchange_rate import CurrencyViewset


currency_router = CurrencyRouter()
currency_router.register('', viewset=CurrencyViewset, basename='currencies')


urlpatterns = [
    path('currencies/', include(currency_router.urls))
]
