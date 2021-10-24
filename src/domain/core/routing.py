# coding: utf-8

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Callable, Union

from src.domain.core.constants import HTTP_VERBS


@dataclass
class Route:
    http_verb: str
    path: str
    controller: Callable
    method: str
    name: str

    def __post_init__(self):
        has_method = hasattr(self.controller, self.method)
        assert has_method, f'Invalid method {self.method} for {self.controller}'
        assert self.http_verb in HTTP_VERBS, f'Invalid http verb {self.http_verb}'

    @property
    def url(self) -> str:
        return self.path

    @property
    def mapping(self) -> dict:
        return {self.http_verb: self.method}


class Router:

    def __init__(self, name: str = None):
        self.name = name
        self.registry = dict()

    def register(self, routes: Union[Iterable, Route]):
        routes = routes if isinstance(routes, Iterable) else [routes]
        for route in routes:
            name = f'{self.name}_{route.name}' if self.name else route.name
            assert name not in self.registry, f'{name} route already registered'
            self.registry.update({name: route})

    def get_route(self, name: str) -> Route:
        return self.registry.get(name) if name in self.registry else None

    def get_url(self, name: str) -> str:
        route = self.get_route(name)
        return route.url if route else None

    def get_urls(self) -> list:
        return [route.url for route in self.registry.values()]

    def map(self, name: str) -> dict:
        route = self.get_route(name)
        return route.mapping if route else None
