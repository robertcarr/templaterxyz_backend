import json

from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from restapi.models import Templates

from utils.drf import APIAdvancedAuth, APIAuthTestCase
from utils.testconfig import TestConfig

class TestSpecificTemplate(APIAuthTestCase):
    """Tests against actions on a specific template"""
    fixtures = ['default']

    def setUp(self):
        self.t = TestConfig()
        self.uuid = self.t.cfg['template']['uuid']
        self.t.set_user('default')
        self.url = f'/api/{self.uuid}/'

    def test_render_with_new_params(self):
        """Can we re-render an existing template with new parameters?"""
        resp = self.client.post(self.url, {
            'params': {'my_name': 'joe'}} , format='json')
        self.assertEqual(resp.data, 'Hey There joe\n', resp.data)

    def test_get_template(self):
        """Can I get a specific template?"""
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['uuid'], self.uuid, resp.data)
        self.assertEqual(resp.content_type, 'application/json', resp.data)

    def test_delete_template(self):
        """Can I delete a template by uuid?"""
        resp = self.client.delete(self.url)
        self.assertEqual(resp.status_code, 204)
        with self.assertRaises(self.t._Templates.DoesNotExist):
            self.t._Templates.objects.get(uuid=self.uuid)

