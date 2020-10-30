from unittest.mock import Mock

from django.test import TestCase
from rest_framework.test import APIRequestFactory, APITestCase
from django.core.files.base import ContentFile, File

from restapi.models import Templates
from utils.render import RenderMixin
from utils.testconfig import TestConfig
from utils.drf import APIAuthTestCase


class TestRenderMixin(APIAuthTestCase):
    """

    """
    fixtures = ['default']

    def setUp(self):
        self.t = TestConfig()

    def test_render(self):
        """Can I re-render a template just with new params?"""
        output = self.t.Template.render({'my_name': 'fly'})
        self.assertEqual(output, 'Hey There fly\n')

    def test_render_string(self):
        """Can I specify a one-off template and params for rendering?"""
        output = self.t.Template.render_string('hi {{name}}', {'name': 'dave'})
        self.assertEqual(output, 'hi dave')


class TestParseParams(APITestCase):
    """
    Test handling of parameter submissions
    """
    fixtures = ['default']
    TEMPLATE = 'my name is {{ name }}'
    PARAMS = '{"name": "joe"}'

    def setUp(self):
        self.template_file = ContentFile(self.TEMPLATE)
        self.param_file = ContentFile(self.PARAMS)
        self.cfg = TestConfig()
        self.req = Mock()
        self.obj = RenderMixin()

    def test_post_files(self):
        """can I post template and params as multipart form files?"""
        self.req.data = {'t': self.template_file, 'p': self.param_file}
        (t, p) = self.obj._parse_query_params(self.req)
        self.assertEqual(t, self.TEMPLATE)
        self.assertEqual(p, self.PARAMS)

    def test_post_files_full(self):
        """can I post template and params as multipart form files using full name?"""
        self.req.data = {'template': self.template_file, 'params': self.param_file}
        (t, p) = self.obj._parse_query_params(self.req)
        self.assertEqual(t, self.TEMPLATE)
        self.assertEqual(p, self.PARAMS)

    def test_post_data(self):
        """Can I post data as content instead of files?"""
        self.req.data = {'t': self.TEMPLATE, 'p': self.PARAMS}
        (t, p) = self.obj._parse_query_params(self.req)
        self.assertEqual(t, self.TEMPLATE)
        self.assertEqual(p, self.PARAMS)

    def test_post_data_full(self):
        """Can I post data as content instead of files with full names?"""
        self.req.data = {'template': self.TEMPLATE, 'params': self.PARAMS}
        (t, p) = self.obj._parse_query_params(self.req)
        self.assertEqual(t, self.TEMPLATE)
        self.assertEqual(p, self.PARAMS)


class TestFiles(APITestCase):
    """
    Strings in/out of File objects
    """
    fixtures = ['default']

    def setUp(self):
        self.cfg = TestConfig()
        self.obj = RenderMixin()
        self.t = self.cfg.cfg['t']
        self.p = self.cfg.cfg['p']

    def test_to_file(self):
        """Can I get a File back from string"""
        f = self.obj.to_file(self.t)
        self.assertIsInstance(f, File)
        contents = f.read()
        self.assertIsInstance(contents, str)
        self.assertEqual(contents, self.t)

    def test_from_file_as_string(self):
        """Can I read file back and get back Str object?"""
        f = self.obj.to_file(self.t)
        contents = self.obj.from_file(f)
        self.assertIsInstance(contents, str, contents)
        self.assertEqual(contents, self.t)
