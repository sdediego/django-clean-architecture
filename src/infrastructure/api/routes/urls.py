# coding: utf-8

from django.conf import settings
from django.conf.urls import include
from django.urls import path


urlpatterns = [
    path('exchange-rates/', include(f'{settings.API_ROUTES}.exchange_rate.urls'))
]
