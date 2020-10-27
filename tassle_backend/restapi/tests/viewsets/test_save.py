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
        self.template = Templates.objects.get(pk=1)


    def test_save_template_returns_url_user(self):
        """Can I save template as a Authenticated User and get a url back?"""

        self.client.set_user(self.User.objects.get(pk=1))
        url = reverse('template-save')
        resp = self.client.post(url,
                         {'template': self.t.template['content'],
                          'params':  self.t.params['content']
                          } )
        self.assertEqual(resp.status_code, 200, resp.data)
        self.assertTrue('url' in resp.data )

