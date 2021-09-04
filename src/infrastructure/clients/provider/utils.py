# coding: utf-8

import datetime
from datetime import datetime as dt

import numpy as np
import pandas as pd


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
