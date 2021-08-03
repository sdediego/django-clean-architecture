# coding: utf-8

import datetime
import string

import factory
from factory import django, fuzzy

from src.infrastructure.orm.db.exchange_rate.models import (
    Currency, CurrencyExchangeRate)


class CurrencyFactory(django.DjangoModelFactory):

    class Meta:
        model = Currency

    code = fuzzy.FuzzyText(length=3, chars=string.ascii_uppercase)
    name = fuzzy.FuzzyText(length=15, chars=string.ascii_letters)
    symbol = fuzzy.FuzzyText(length=1)


class CurrencyExchangeRateFactory(django.DjangoModelFactory):

    class Meta:
        model = CurrencyExchangeRate

    source_currency = factory.SubFactory(CurrencyFactory)
    exchanged_currency = factory.SubFactory(CurrencyFactory)
    valuation_date = fuzzy.FuzzyDate(
        datetime.date.today() + datetime.timedelta(days=-10),
        datetime.date.today())
    rate_value = fuzzy.FuzzyDecimal(0.5, 1.5)
