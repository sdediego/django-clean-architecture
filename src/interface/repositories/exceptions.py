# coding: utf-8

class EntityError(Exception):

    def __init__(self, message: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message

    def __str__(self) -> str:
        return f'{self.__class__.__name__}: {self.message}'


class EntityDoesNotExist(EntityError):
    pass
