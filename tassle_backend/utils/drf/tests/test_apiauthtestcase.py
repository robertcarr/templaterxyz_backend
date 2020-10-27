from django.test import TestCase
from django.conf import settings

from django.contrib.auth import get_user_model

from utils.drf import APIAuthTestCase, APIAdvancedAuth


class TestClass(TestCase):
    """

    """
    fixtures = ['default']

    def setUp(self):
        self.obj = APIAuthTestCase()

    def test_client(self):
        """Are we using our custom auth client?"""
        self.assertIsInstance(self.obj.client, APIAdvancedAuth)

    def test_has_user(self):
        """Has user attribute?"""
        self.assertTrue(self.obj.User)

    def test_can_set_user(self):
        """Can set a user"""
        self.obj.client.set_user(self.obj.User.objects.get(pk=1))
        self.assertEqual(self.obj.client.current_user, self.obj.User.objects.get(pk=1))
