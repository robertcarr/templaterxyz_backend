import json

from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from restapi.models import Templates

from utils.drf import APIAdvancedAuth, APIAuthTestCase


class TestEdit(APIAuthTestCase):
    """Saving/Editing a Template should return a valid URL to the template"""
    fixtures = ['default']

    def setUp(self):
        self.t = Templates.objects.get(pk=1)

    def test_save_template_returns_url(self):
        t_file = ContentFile('my template')
        t_params = ContentFile('my params')

        self.client.set_user(self.User.objects.get(pk=1))
        url = reverse('template-save')
        resp = self.client.post(url,
                         {'template': t_file,
                          'params': t_params}
                                )
        self.assertEqual(resp.status_code, 200, resp.data)
        self.assertTrue('url' in resp.data )

