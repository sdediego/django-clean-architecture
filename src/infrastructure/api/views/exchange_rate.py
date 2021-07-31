# coding: utf-8

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class CurrencyViewSet(ViewSet):
    viewset_factory = None

    def get(self, request: Request, code: str, *args, **kwargs) -> Response:
        payload, status = self.viewset_factory.create().get(code)
        return Response(data=payload, status=status)

    def list(self, request: Request, *args, **kwargs) -> Response:
        payload, status = self.viewset_factory.create().list()
        return Response(data=payload, status=status)


class CurrencyExchangeRateViewSet(ViewSet):
    viewset_factory = None

    def convert(self, request: Request, *args, **kwargs) -> Response:
        query_params = request.query_params
        payload, status = self.viewset_factory.create().convert(query_params)
        return Response(data=payload, status=status)

    def list(self, request: Request, *args, **kwargs) -> Response:
        query_params = request.query_params
        payload, status = self.viewset_factory.create().list(query_params)
        return Response(data=payload, status=status)

    def calculate_twr(self, request: Request, *args, **kwargs) -> Response:
        query_params = request.query_params
        payload, status = self.viewset_factory.create().calculate_twr(query_params)
        return Response(data=payload, status=status)
