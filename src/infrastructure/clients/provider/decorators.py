# encoding: utf-8

import asyncio
from functools import wraps


def async_event_loop(method):
    @wraps(method)
    def result(self, *args, **kwargs):
        response = asyncio.run(method(self, *args, **kwargs))
        return response
    return result
