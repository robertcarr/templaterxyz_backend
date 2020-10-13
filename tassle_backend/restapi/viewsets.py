from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_cognito_jwt import JSONWebTokenAuthentication

from restapi.exceptions import MissingTemplateOrParams, TemplateNotFound
from utils.render import PlainTextRenderer
from .models import Templates
from .serializers import TemplatesSerializer


class TemplateViewset(viewsets.ModelViewSet):
    model = Templates
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'
    serializer_class = TemplatesSerializer
    renderer_classes = [PlainTextRenderer, JSONRenderer]
    http_method_names = ['post', 'delete', 'get']

    def create(self, request, **kwargs):
        """
        Post a new template as form file fields.  By default, we don't save this so it's
        fast and we don't waste space with lots of junk templates that need to be purged later.

        template=File
        params=File
        :param request:
        :param kwargs:
        :return:
        """
        print(request.query_params)
        t = Templates()
        t.parse_request(request)
        return Response(t.render(), content_type='text/plain')

    def retrieve(self, request, uuid=None, **kwargs):
        """
        Get a specific template by uuid
        :param request:
        :param uuid:
        :param kwargs:
        :return: Template data
        """
        try:
            t = Templates.objects.get(uuid=uuid)
        except Templates.DoesNotExist:
            raise TemplateNotFound
        return Response(t.get_template, content_type='text/plain')

    @action(methods=['post'], detail=False)
    def edit(self, request, *kwargs):
        """
        User wants to edit a template so we return the details & URL
        :param request:
        :param kwargs:
        :return: link to template editor for this template
        """
        t = Templates()
        t.parse_request(request)
        t.save()
        t_serializer = TemplatesSerializer(t)
        return Response(t_serializer.data)

    def get_queryset(self):
        return self.model.objects.all()
