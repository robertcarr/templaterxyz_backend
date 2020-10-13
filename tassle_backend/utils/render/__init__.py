import json

import jinja2
from rest_framework import renderers
from django.utils.encoding import smart_text


class RenderMixin:
    """
    """
    engine = None

    def render(self, params=None):
        """
        :return: render template as String
        """
        if self.template.tell() > 0:
            self.template.seek(0)

        t = jinja2.Template(self.template.read().decode('utf-8'))
        self.template.seek(0)
        if params:
            self._rendered_template = t.render(params)
        else:
            params = self.params.read().decode('utf-8')
            self._rendered_template = t.render(json.loads(params))
        return self._rendered_template


class PlainTextRenderer(renderers.BaseRenderer):
    """
    Return plain/text response body that handles NEWLINE instead of printing /n
    """
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, media_type=None, renderer_context=None):
        return smart_text(data, encoding=self.charset)
