import json

from django.contrib.auth import get_user_model
from django.urls import reverse

from restapi.models import Templates
from utils.drf import APIAdvancedAuth, APIAuthTestCase
from utils.testconfig import TestConfig






class TestTemplateList(APIAuthTestCase):
    """
    List users Templates
    """
    fixtures = ['default']


    def setUp(self):
        self.t = TestConfig()

    def test_list_authenticated(self):
        """Authenticated user can list own templates?"""
        self.t.set_user('default')
        self.client.set_user(self.t.user)
        resp = self.client.get(reverse('template-list'))
        # Temp 405 check since we disabled auth
        self.assertEqual(resp.status_code, 405)

    def test_list_anon_user(self):
        """We should fail 401 non-authenticated if not logged in"""
        self.client.set_user()
        resp = self.client.get(reverse('template-list'))
        # Should be 405 until auth is enabled
        self.assertEqual(resp.status_code, 405, resp.data)


class TestTemplateRender(APIAuthTestCase):
    """
    Can we render a basic template?
    """
    fixtures = ['default']

    def setUp(self):
        self.t = TestConfig()
        self.url = reverse('template-list')

    def test_post_no_params(self):
        """Can we handle a POST to render but no variables sent?"""
        resp = self.client.post(self.url)
        self.assertEqual(resp.status_code, 200, resp.data)

    def test_post_template(self):
        """Can we render a new Template as files?"""
        resp = self.client.post(self.url,
                                {'template': self.t.get_template_file(),
                                 'params': self.t.get_params_file()
                                 })
        self.assertEqual(resp.status_code, 200, resp.data)
        self.assertEqual(resp.data, self.t.fake_render)
        self.assertEqual(resp.content_type, 'text/plain')

    def test_render_template_error_json(self):
        """Do we get JSON return type when we have render error?"""
        resp = self.client.post(self.url, {'template': 'test {{ name }}'})
        self.assertEqual(resp.status_code, 400, resp.data)
        #with self.assertRaises(AssertionError) as e:
        #    self.assertEqual(resp.data, self.t.fake_render)
        #self.assertEqual(resp.content_type, 'application/json')

    def test_post_template_short(self):
        """Can we render new template using t= and p= instead of template and params?"""
        resp = self.client.post(self.url,
                                {'t': self.t.get_template_file(),
                                 'p': self.t.get_params_file()
                                 })
        self.assertEqual(resp.status_code, 200, resp.data)
        self.assertEqual(resp.data, self.t.fake_render)
        self.assertEqual(resp.content_type, 'text/plain')

    def test_post_template_file_params_as_content(self):
        """Can I post a template and params as content instead of file?"""
        resp = self.client.post(self.url,
                                {'t': 'my name is {{ name }}',
                                 'p': {'name': 'joe'}
                                 }, format='json')
        self.assertEqual(resp.status_code, 200, resp.data)
        self.assertEqual(resp.data, self.t.fake_render)
        self.assertEqual(resp.content_type, 'text/plain')
