# coding: utf-8

from typing import Callable

import pytest

from src.domain.core.routing import Route
from tests.fixtures import route, router


@pytest.mark.unit
def test_route_attrs(route):
    assert isinstance(route.http_verb, str)
    assert isinstance(route.path, str)
    assert isinstance(route.controller, Callable)
    assert isinstance(route.method, str)
    assert isinstance(route.name, str)


@pytest.mark.unit
def test_route_url_property(route):
    assert hasattr(route, 'url')
    assert route.path == route.url


@pytest.mark.unit
def test_route_mapping_property(route):
    assert hasattr(route, 'mapping')
    assert route.mapping == {route.http_verb: route.method}


@pytest.mark.unit
def test_route_invalid_http_verb(route):
    invalid_http_verb = 'invalid_http_verb'
    error_message = f'Invalid http verb {invalid_http_verb}'
    with pytest.raises(AssertionError) as err:
        Route(
            http_verb=invalid_http_verb,
            path=route.path,
            controller=route.controller,
            method=route.method,
            name=route.name
        )
    assert error_message in str(err.value)


@pytest.mark.unit
def test_route_invalid_method(route):
    fake_method = 'fake_method'
    error_message = f'Invalid method {fake_method} for {route.controller}'
    with pytest.raises(AssertionError) as err:
        Route(
            http_verb=route.http_verb,
            path=route.path,
            controller=route.controller,
            method=fake_method,
            name=route.name
        )
    assert error_message in str(err.value)


@pytest.mark.unit
def test_router_registry(route, router):
    assert isinstance(router.registry, dict)
    assert route.name in router.registry


@pytest.mark.unit
def test_router_invalid_duplicate_route_in_registry(route, router):
    error_message = f'{route.name} route already registered'
    assert route.name in router.registry
    with pytest.raises(AssertionError) as err:
        router.register(route)
    assert error_message in str(err.value)


@pytest.mark.unit
def test_router_get_route(route, router):
    invalid_route_name = 'fake_route'
    assert router.get_route(route.name) == route
    assert router.get_route(invalid_route_name) is None


@pytest.mark.unit
def test_router_get_url(route, router):
    invalid_route_name = 'fake_route'
    assert router.get_url(route.name) == route.url
    assert router.get_route(invalid_route_name) is None


@pytest.mark.unit
def test_router_get_urls(route, router):
    assert router.get_urls() == [route.url]


@pytest.mark.unit
def test_router_map(route, router):
    invalid_route_name = 'fake_route'
    assert router.map(route.name) == {route.http_verb: route.method}
    assert router.map(invalid_route_name) is None
