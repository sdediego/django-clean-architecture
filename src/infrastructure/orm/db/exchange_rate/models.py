# coding: utf-8

from django.db import models

from src.domain.exchange_rate import CurrencyEntity, CurrencyExchangeRateEntity


class Currency(models.Model):
    code = models.CharField(max_length=3, primary_key=True, unique=True)
    name = models.CharField(max_length=25, db_index=True)
    symbol = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        verbose_name = 'currency'
        verbose_name_plural = 'currencies'
        ordering = ('code',)

    def __str__(self) -> str:
        return CurrencyEntity.to_string(self)


class CurrencyExchangeRate(models.Model):
    source_currency = models.ForeignKey(
        Currency, db_index=True, on_delete=models.CASCADE, related_name='exchanges')
    exchanged_currency = models.ForeignKey(
        Currency, db_index=True, on_delete=models.CASCADE)
    valuation_date = models.DateField(db_index=True)
    rate_value = models.DecimalField(decimal_places=6, max_digits=18)

    class Meta:
        verbose_name = 'currency exchange rate'
        verbose_name_plural = 'currency exchange rates'
        ordering = ('-valuation_date', 'source_currency')

    def __str__(self) -> str:
        return CurrencyExchangeRateEntity.to_string(self)
