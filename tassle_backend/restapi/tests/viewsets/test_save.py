import json

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
        self.assertTrue('url' in resp.data )

    def test_save_template_returns_non_auth(self):
        """Can I save a template without auth?"""
        self.client.set_user()
        resp = self.client.post(self.url,
                                {'template': self.t.get_template_file(),
                                 'params': self.t.get_params_file()})
        self.assertEqual(resp.status_code, 200, resp.data)
        self.assertTrue('url' in resp.data)

