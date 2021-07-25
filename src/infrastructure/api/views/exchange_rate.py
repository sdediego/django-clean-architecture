# coding: utf-8

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class CurrencyViewset(GenericViewSet):
    view_factory = None

    def get(self, request: Request, *args, **kwargs) -> Response:
        code = request.query_params.get('code')
        body, status = self.view_factory.create().get(code)
        return Response(data=body, status=status)

    def list(self, request: Request, *args, **kwargs) -> Response:
        body, status = self.view_factory.create().list()
        return Response(data=body, status=status)
