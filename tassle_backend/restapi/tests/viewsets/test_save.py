import json
from time import sleep

from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from restapi.models import Templates

from utils.drf import APIAdvancedAuth, APIAuthTestCase
from utils.testconfig import TestConfig


class TestEdit(APIAuthTestCase):
    """Saving/Editing a Template should return a valid URL to the template"""
    fixtures = ['default']

    def setUp(self):
        self.t = TestConfig()
        self.t.set_user('default')
        self.url = reverse('template-save')

    def test_save_template_returns_url_user(self):
        """Can I save template as a Authenticated User and get a url back?"""

        resp = self.client.post(self.url,
                         {'template': self.t.get_template_file(),
                          'params':  self.t.get_params_file()
                          } )
        self.assertEqual(resp.status_code, 200, resp.data)
        self.assertEqual(resp.content_type, 'application/json')
        self.assertTrue('url' in resp.data)

        # Check we actually save a template and it's the right data
        uuid = resp.data['url'][-22:]
        template = self.t._Templates.objects.get(uuid=uuid)
        f2 = template.template.read().decode('utf-8')
        f1 = self.t.get_template_file().read()
        self.assertEqual(f1, f2, f'Template Files do not match={f2}')

    def test_save_template_returns_non_auth(self):
        """Can I save a template without auth?"""
        self.client.set_user()
        resp = self.client.post(self.url,
                                {'template': self.t.get_template_file(),
                                 'params': self.t.get_params_file()})
        self.assertEqual(resp.status_code, 200, resp.data)
        self.assertTrue('url' in resp.data)

    def test_save_template_without_params(self):
        """Save without params should just write template"""
        resp = self.client.post(self.url,
                                {'template': self.t.get_template_file()})
        self.assertEqual(resp.status_code, 200, resp.data)
        self.assertTrue('url' in resp.data, resp.data )
        t = self.t.Template.template
        self.assertTrue(t, self.t.get_template_file())
