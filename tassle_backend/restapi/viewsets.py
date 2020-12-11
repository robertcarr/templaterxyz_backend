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
from django.http import HttpResponse
from django.core.mail import send_mail

from restapi.exceptions import MissingTemplateOrParams, TemplateNotFound, MissingParameters, AccountRequired, \
    TemplateInvalidOrMissing
from utils.render import PlainTextRenderer
from utils.drf.content import CustomContentNegotiation
from .models import Templates, Stats
from .serializers import TemplatesSerializer, StatsSerializer

log = logging.getLogger(__name__)



def update_template_stats():
    """
    Update the stats for number of rendered templates
    :return: None
    """
    stats = Stats.objects.filter(id=1)
    stats.update(templates_rendered=F('templates_rendered') + 1)

class FeedbackViewset(viewsets.ViewSet):
    """
    Accept Feedback and send as email
    """
    http_method_names = ['post']
    permission_classes = [AllowAny]
    authentication_classes = []

    def create(self, request, **kwargs):
        """ POST new feedback"""
        msg = request.data.get('msg')
        if msg:
            print(msg)
            send_mail('Templater Feedback', json.dumps(msg), 'admin@clientless.io', ['carrenator@gmail.com'])
        return Response(status=200)

class StatsViewset(viewsets.ModelViewSet):
    """
    Return template stats for the homepage
    """
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
    renderer_classes = [JSONRenderer, PlainTextRenderer]
    authentication_classes = []
    # authentication_classes = [TokenAuthentication, JSONWebTokenAuthentication]
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'put']

    def list(self, request):
        """
        If logged in, return your some template details otherwise raise exception
        :param request:
        :return:
        """
        msg = {'detail': 'see https://templater.xyz for help'}
        return Response(msg, content_type='application/json')

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
        update_template_stats()
        try:
            (template, params) = t.parse_request(request)
        except AssertionError:
            raise MissingTemplateOrParams

        rendered_t = t.render_string(template, params)
        return HttpResponse(rendered_t, content_type='text/plain')

    def update(self, request, uuid=None):
        """ Render and Existing Template but with new parameters """
        update_template_stats()
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
        return HttpResponse(t.get_template, content_type='text/plain')

    @action(methods=['post'], detail=False, renderer_classes=[JSONRenderer])
    def share(self, request, *kwargs):
        """
        User wants to edit a template so we save the template and any parameters
        and return the URL to edit it.  If a template is saved without parameters being passed in
        any exiting file associated with it is deleted.

        :param request:
        :param kwargs:
        :return: link to template editor for this template
        """
        update_template_stats()
        t = Templates()
        (template_data, params_data) = t.parse_request(request)
        t.template = t.to_file(template_data, 'template.j2', encoding='utf-8')
        if params_data:
            t.params = t.to_file(params_data, 'params.json', encoding='utf-8')
        else:
            t.params.delete()
        t.save()
        serializer = TemplatesSerializer(t)
        return Response({
            'ui_url': f'https://templater.xyz/{t.uuid}',
            'api_url': t.get_url(),
            'template_id': t.uuid},
            content_type='application/json', status=200)

    @action(methods=['get'], detail=True)
    def dump(self, request, uuid=None):
        """ Dump the template and params in JSON format"""

        update_template_stats()
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

        update_template_stats()
        """Creating on an existing Template should render the template with new params"""
        try:
            t = Templates.objects.get(uuid=uuid)
        except Templates.DoesNotExist:
            raise TemplateNotFound

        (template_data, param_data) = t._parse_query_params(request)
        # If we are passed in a new Template, lets save this updated template first.
        # this will overwrite the original template.  Need to clean this up a bit.  Messy.
        if template_data:
            f = t.to_file(template_data, encoding='utf-8')
            t.template.save('t', f, save=True)
            # Hokey but if it's template only return OK 200 after saving the new template
            if not param_data:
                return Response(status=200)
        # Re-render the template with parameters if supplied.  If none supplied, use any saved params
        if param_data:
            try:
                rendered_template = t.render(param_data)
                return HttpResponse(rendered_template, content_type='text/plain', status=200)
            except KeyError:
                raise MissingParameters
        else:
            raise MissingParameters

    def retrieve(self, request, uuid=None, renderer_classes=[PlainTextRenderer], **kwargs):
        # TODO: Check ownership
        update_template_stats()
        try:
            t = Templates.objects.get(uuid=uuid)
            serializer = TemplatesSerializer(t)
        except Templates.DoesNotExist:
            raise TemplateNotFound
        print(serializer.data)
        try:
            # If we ask for params in the UI, we want to return them and respond as JSON
            if request.query_params.get('details'):
                return Response(serializer.data, content_type='application/json')
            return HttpResponse(serializer.data['template'], content_type='text/plain')
            return Response(serializer.data['template'], content_type='text/plain')
        except ValueError as e:
            raise TemplateInvalidOrMissing

    @action(methods=['get'], detail=True, renderer_classes=[JSONRenderer])
    def details(self, request, uuid=None, **kwargs):
        """Get Detailed info about a template"""
        update_template_stats()
        try:
            t = Templates.objects.get(uuid=uuid)
            serializer = TemplatesSerializer(t)
        except Templates.DoesNotExist:
            raise TemplateNotFound
        return Response(serializer.data, content_type='application/json')
