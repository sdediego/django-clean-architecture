# coding: utf-8

class EntityError(Exception):

    def __init__(self, message: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message


class EntityDoesNotExist(EntityError):
    pass
