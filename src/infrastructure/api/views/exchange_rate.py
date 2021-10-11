# coding: utf-8

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from src.interface.controllers.exchange_rate import (
    CurrencyController, CurrencyExchangeRateController)


class CurrencyViewSet(ViewSet):
    viewset_factory = None

    @property
    def controller(self) -> CurrencyController:
        return self.viewset_factory.create()

    def get(self, request: Request, code: str, *args, **kwargs) -> Response:
        payload, status = self.controller.get(code)
        return Response(data=payload, status=status)

    def list(self, request: Request, *args, **kwargs) -> Response:
        payload, status = self.controller.list()
        return Response(data=payload, status=status)


class CurrencyExchangeRateViewSet(ViewSet):
    viewset_factory = None

    @property
    def controller(self) -> CurrencyExchangeRateController:
        return self.viewset_factory.create()

    def convert(self, request: Request, *args, **kwargs) -> Response:
        query_params = request.query_params
        payload, status = self.controller.convert(query_params)
        return Response(data=payload, status=status)

    def list(self, request: Request, *args, **kwargs) -> Response:
        query_params = request.query_params
        payload, status = self.controller.list(query_params)
        return Response(data=payload, status=status)

    def calculate_twr(self, request: Request, *args, **kwargs) -> Response:
        query_params = request.query_params
        payload, status = self.controller.calculate_twr(query_params)
        return Response(data=payload, status=status)
