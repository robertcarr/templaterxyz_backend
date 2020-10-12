from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_cognito_jwt import JSONWebTokenAuthentication

from .models import Templates


class TemplateViewset(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def list(self, request):
        return Response("Hey")

    def create(self, request, **kwargs):
        """
        Post a new template as form file fields
        template=File
        params=File

        :param request:
        :param kwargs:
        :return:
        """



