import json

from django.contrib.auth import get_user_model
from django.urls import reverse

from restapi.models import Templates
from utils.drf import APIAdvancedAuth, APIAuthTestCase


class TestTemplateList(APIAuthTestCase):
    """
    List users Templates
    """
    fixtures = ['default']


    def test_list_authenticated(self):
        """Authenticated user can list own templates?"""
        self.client.set_user(self.User.objects.get(pk=1))
        resp = self.client.get(reverse('template-list'))
        self.assertEqual(resp.status_code, 200)

    def test_list_anon_user(self):
        """We should fail 401 non-authenticated if not logged in"""
        self.client.set_user()
        resp = self.client.get(reverse('template-list'))
        self.assertEqual(resp.status_code, 401)

