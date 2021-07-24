# coding: utf-8

from django.db import models


class Currency(models.Model):
    code = models.CharField(max_length=3, primary_key=True, unique=True)
    name = models.CharField(max_length=25, db_index=True)
    symbol = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        verbose_name = 'currency'
        verbose_name_plural = 'currencies'
        ordering = ('code',)
