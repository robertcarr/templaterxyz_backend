import json
import logging

import jinja2
from jinja2 import Template as JinjaTemplate, StrictUndefined
from jinja2.exceptions import UndefinedError, TemplateSyntaxError as JinjaTemplateSyntaxError
from rest_framework import renderers
from django.utils.encoding import smart_text
from django.core.files.base import ContentFile, File
from django.core.files.uploadedfile import InMemoryUploadedFile

from restapi.exceptions import InvalidParameterFormat, MissingParameters, TemplateSyntaxError

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

log = logging.getLogger(__name__)

class RenderMixin:
    """
    """
    engine = None

    def parse_request(self, request):
        """ Takes request and modifies the template instance with User, Files
        returns (template, params) as strings
         """
        if request.user.is_anonymous:
            self.user = None
        else:
            self.user = request.user
        return self._parse_query_params(request)

    @property
    def get_template(self):
        return self._read_template()

    @property
    def get_params(self):
        return self._read_params()

    def from_file(self, fileobj, encoding='utf-8'):
        """
        Decode from file back into string
        :param fileobj: File object
        :param encoding:
        :return: string
        """
        assert (isinstance(fileobj, File)), "Must be File type object"
        with fileobj.open() as f:
            contents = f.read()
        if isinstance(contents, bytes):
            return contents.decode(encoding)
        else:
            return contents
        #return fileobj.read()

    def to_file(self, data, filename='template.j2', encoding=None):
        """
        Returns a ContentFile from the string of data or a Dict which is converted via JSON dumps
        :param encoding: Encoding format
        :param filename: string filename
        :param data: string or Dict
        :return: ContentFile
        """
        if isinstance(data, dict):
            data = json.dumps(data)
        assert (isinstance(data, str)), "Must be String"
        if encoding:
            data = data.encode(encoding)
        f = ContentFile(data)
        f.name = filename
        return f

    def _parse_query_params(self, request, raise_for_missing=False):
        """
        Take the submitted queryparams data and return the template and params as a Dict
        :param request:
        :return: (template string, params as Dict)
        """
        # Accept Files named 'template' or 't' for short, 'params' and 'p'
        template_data = request.data.get('template', request.data.get('t', ""))
        param_data = request.data.get('params', request.data.get('p', {}))

        if isinstance(template_data, list):
            template_data = template_data[0]
        if isinstance(template_data, File):
            template_data = self.from_file(template_data)
        if isinstance(param_data, File):
            param_data = self.from_file(param_data)
        if isinstance(param_data, str):
            param_data = json.loads(param_data)

        # Return template_data as String and Params as Dict
        return (template_data, param_data)

    def _update_params(self, param_file):
        """ Update the params file object """
        self.params = param_file

    def _read_template(self):
        """ Read in raw template from storage and return text of template """
        # Reset to beginning of file if it's been read already
        return self.from_file(self.template)

    def _read_params(self):
        """Read parameters from storage and return as DICT """
        params = self.from_file(self.params)

        try:
            params = json.loads(params)
        except json.JSONDecodeError:
            raise InvalidParameterFormat(params)
        return params

    def _render_template(self, template="", params={}, **kwargs):
        """
        Actually Renders the template with parameters
        :param template: String
        :param params:  Dict
        :return:  String of rendered template
        """
        render_options = {}
        assert isinstance(params, dict), f'Params not a valid Dict: {params}'
        assert isinstance(template, str), f'Template must be string: {template}'
        if kwargs.get('undefined') == 'raise':
            render_options = {'undefined': StrictUndefined}
        try:
            rendered_template = jinja2.Template(template, **render_options).render(params)
        except (UndefinedError) as e:
            raise MissingParameters(e)
        except (TypeError, JinjaTemplateSyntaxError) as e:
            raise TemplateSyntaxError(detail=e)
        return rendered_template

    def render_string(self, template, params, **kwargs):
        """
        Render a template as string with dict params
        :param template:
        :param params: Dict
        :return: merged template as string
        """
        return self._render_template(template, params, **kwargs)

    def render(self, params=None):
        """
        Takes a Dict of params and re-renders the already existing Template

        :param params: Dict of Jinja Params to replace, re-rendering using existing params if none supplied
        :return: render template as String

        TODO: More error checking and possibilities here
        """
        if not params:
            params = self._read_params()
        template = self._read_template()

        return self.render_string(template, params)

class PlainTextRenderer(renderers.BaseRenderer):
    """
    Return plain/text response body that handles NEWLINE instead of printing /n
    """
    media_type = 'text/plain'
    format = 'txt'
    render_style = 'text'

    def render(self, data, media_type=None, renderer_context=None):
        return smart_text(data, encoding=self.charset)
