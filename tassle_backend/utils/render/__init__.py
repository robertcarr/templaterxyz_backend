import json

import jinja2
from jinja2 import Template, StrictUndefined
from jinja2.exceptions import UndefinedError
from rest_framework import renderers
from django.utils.encoding import smart_text

from restapi.exceptions import InvalidParameterFormat, MissingParameters

class BaseTemplateRenderer:
    """

    """
    def __init__(self, *args, **kwargs):
        self._template = kwargs.pop('template', None)

    def render(self, params):
        """
        Render the template with a set of JSON parameters
        :param params:  Dict of Parameters
        :return: string of merged template
        """


class RenderMixin:
    """
    """
    engine = None

    @property
    def get_template(self):
        return self._read_template()

    @property
    def get_params(self):
        return self._read_params()

    def _update_params(self, param_file):
        """ Update the params file object """
        self.params = param_file

    def _read_template(self):
        """ Read in raw template from storage and return text of template """
        # Reset to beginning of file if it's been read already
        if self.template.tell() > 0:
            self.template.seek(0)
        template = self.template.read().decode('utf-8')
        self.template.seek(0) # return to beginning
        return template

    def _read_params(self):
        """Read parameters from storage and return as DICT """
        if self.params.tell() > 0:
            self.params.seek(0)
        params = self.params.read().decode('utf-8')
        self.params.seek(0)
        try:
            params = json.loads(params)
        except json.JSONDecodeError:
            raise InvalidParameterFormat
        return params

    def render_string(self, template, params):
        """
        Render a template as string with dict params
        :param template:
        :param params:
        :return: merged template as string
        """
        t = jinja2.Template(template)
        return t.render(params)

    def render(self, params=None, undefined=StrictUndefined):
        """
        :return: render template as String

        TODO: More error checking and possibilities here
        """
        # undefined=StrictUndefined
        t = Template(self._read_template(), undefined=undefined)
        try:
            if params:
                self._rendered_template = t.render(params)
            else:
                self._rendered_template = t.render(self._read_params())
        except UndefinedError as e:
            raise MissingParameters(e)
        return self._rendered_template


class PlainTextRenderer(renderers.BaseRenderer):
    """
    Return plain/text response body that handles NEWLINE instead of printing /n
    """
    media_type = 'text/plain'

    def render(self, data, media_type=None, renderer_context=None):
        return smart_text(data, encoding=self.charset)
