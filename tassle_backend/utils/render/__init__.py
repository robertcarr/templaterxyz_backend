import json

import jinja2
from rest_framework import renderers
from django.utils.encoding import smart_text

from restapi.exceptions import InvalidParameterFormat


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

    def render(self, params=None):
        """
        :return: render template as String

        TODO: More error checking and possibilities here
        """
        t = jinja2.Template(self._read_template())
        if params:
            self._rendered_template = t.render(params)
        else:
            self._rendered_template = t.render(self._read_params())
        return self._rendered_template


class PlainTextRenderer(renderers.BaseRenderer):
    """
    Return plain/text response body that handles NEWLINE instead of printing /n
    """
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, media_type=None, renderer_context=None):
        return smart_text(data, encoding=self.charset)
