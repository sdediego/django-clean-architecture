# coding: utf-8

import datetime
from datetime import datetime as dt
from importlib import import_module

import numpy as np
import pandas as pd


def get_available_drivers() -> dict:
    try:
        module = import_module('src.infrastructure.clients.provider')
    except ImportError:
        raise ImportError('Unable to import providers module')
    drivers = {
        name: item for name, item in module.__dict__.items() \
            if name.endswith('Driver') and callable(item)
    }
    return drivers


def get_drivers_names() -> tuple:
    return tuple(get_available_drivers().keys())


def get_drivers_choices() -> tuple:
    return tuple(zip(*(get_drivers_names(),) * 2))


def get_business_days(date_from: str, date_to: str) -> tuple:
    bdays = pd.bdate_range(start=date_from, end=date_to).values
    return tuple([np.datetime_as_string(bday, unit='D') for bday in bdays])


def get_last_business_day(date: str = None) -> str:
    date = date or datetime.date.today().strftime('%Y-%m-%d')
    is_business_day = bool(len(pd.bdate_range(start=date, end=date)))
    if not is_business_day:
        offset = pd.tseries.offsets.BusinessDay(n=1)
        date = (dt.strptime(date, '%Y-%m-%d') - offset).strftime('%Y-%m-%d')
    return date
