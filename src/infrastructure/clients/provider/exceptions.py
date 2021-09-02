# coding: utf-8

class ProviderDriverError(Exception):

    def __init__(self, message: str, code: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message
        self.code = code
