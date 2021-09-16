# coding: utf-8

import os

from celery import Celery


env = os.environ.get('DJANGO_ENV')
settings_module = f'src.infrastructure.settings.{env}'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

app = Celery('forex')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
