import json
import logging

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_cognito_jwt import JSONWebTokenAuthentication
from django.db.models import F
from jinja2 import exceptions as jinja2_exceptions

from restapi.exceptions import MissingTemplateOrParams, TemplateNotFound, MissingParameters, AccountRequired
from utils.render import PlainTextRenderer
from .models import Templates, Stats
from .serializers import TemplatesSerializer, StatsSerializer

log = logging.getLogger(__name__)


class StatsViewset(viewsets.ModelViewSet):
    model = Stats
    serializer_class = StatsSerializer
    http_method_names = ['get']
    permission_classes = [AllowAny]

    def list(self, request):
        stats = Stats.objects.get(id=1)
        serializer = StatsSerializer(stats)
        return Response(serializer.data)


class TemplateViewset(viewsets.ModelViewSet):
    model = Templates
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'
    serializer_class = TemplatesSerializer
    renderer_classes = [PlainTextRenderer, JSONRenderer, PlainTextRenderer]
    authentication_classes = [TokenAuthentication, JSONWebTokenAuthentication]
    permission_classes = [AllowAny]
    http_method_names = ['post', 'delete', 'get', 'put']

    def list(self, request):
        """
        If logged in, return your some template details otherwise raise exception
        :param requset:
        :return:
        """
        if request.user.is_anonymous:
            raise AccountRequired
        # For now just dump all their templates
        serializer = TemplatesSerializer(self.get_queryset(), many=True)

        return Response(serializer.data)

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
        t = Templates()
        (template, params) = t.parse_request(request)
        stats = Stats.objects.filter(id=1)
        stats.update(templates_rendered=F('templates_rendered') + 1)
        rendered_t = t.render_string(template, params)
        return Response(rendered_t, content_type='text/plain')

    def update(self, request, uuid=None):
        """ Render and Existing Template but with new parameters """
        try:
            t = Templates.objects.get(uuid=uuid)
            try:
                t._update_params(request.FILES['params'])
            except KeyError:
                raise MissingParameters
        except Templates.DoesNotExist:
            raise TemplateNotFound
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
    def save(self, request, *kwargs):
        """
        User wants to edit a template so we return the details & URL
        :param request:
        :param kwargs:
        :return: link to template editor for this template
        """
        t = Templates()
        t.parse_request(request)
        t.save()
        serializer = TemplatesSerializer(t)
        return Response({'url': t.get_url()})

    @action(methods=['get'], detail=True)
    def dump(self, request, uuid=None):
        """ Dump the template and params in JSON format"""
        try:
            t = Templates.objects.get(uuid=uuid)
            template_info = {'template': t.template,
                             'params': t.params}
            serializer = TemplatesSerializer(t)
            return Response(t.data)
        except t.DoesNotExist:
            raise TemplateNotFound

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TemplateDetailViewset(DestroyModelMixin, viewsets.GenericViewSet):
    """
    Handle a specific Template by UUID

    GET: Return Template & Metadata
    POST: Rerender with new params
    PUT: Update existing template
    DELETE: Delete
    """
    http_method_names = ['post', 'get', 'delete', 'put']
    lookup_value_regex = '[0-9a-zA-Z]{22}'
    lookup_url_kwarg = 'uuid'
    lookup_field = 'uuid'
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = Templates.objects.all()

    def post(self, request, uuid=None, **kwargs):
        """Creating on an existing Template should render the template with new params"""
        try:
            t = Templates.objects.get(uuid=uuid)
        except Templates.DoesNotExist:
            raise TemplateNotFound
        (template_data, param_data) = t._parse_query_params(request)
        try:
            rendered_template = t.render(param_data)
            return Response(rendered_template, content_type='text/plain', status=200)
        except KeyError:
            raise MissingParameters

    def retrieve(self, request, uuid=None, **kwargs):
        # TODO: Check ownership
        try:
            t = Templates.objects.get(uuid=uuid)
            serializer = TemplatesSerializer(t)
        except t.DoesNotExist:
            raise TemplateNotFound
        return Response(serializer.data, content_type='application/json')


