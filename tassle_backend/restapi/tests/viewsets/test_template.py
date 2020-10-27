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
        self.assertEqual(resp.status_code, 200)

    def test_list_anon_user(self):
        """We should fail 401 non-authenticated if not logged in"""
        self.client.set_user()
        resp = self.client.get(reverse('template-list'))
        self.assertEqual(resp.status_code, 401, resp.data)


class TestTemplateRender(APIAuthTestCase):
    """
    Can we render a basic template?
    """
    fixtures = ['default']

    def setUp(self):
        self.t = TestConfig()
        self.url = reverse('template-list')

    def test_post_template(self):
        """Can we render?"""
        resp = self.client.post(self.url,
                                {'template': self.t.template['content'],
                                 'params': self.t.params['content']
                                 })
        self.assertEqual(resp.status_code, 200, resp.data)
        self.assertEqual(resp.data, 'My name is test_user')
        self.assertEqual(resp.content_type, 'text/plain')

