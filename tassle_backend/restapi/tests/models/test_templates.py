from django.test import TestCase

from restapi.models import Templates
from utils.testconfig import TestConfig


class TestTemplates(TestCase):
    fixtures = ['default']

    def setUp(self):
        self.cfg = TestConfig()

    def test_is_public(self):
        """Does is_public match Template?"""
        self.assertEqual(self.cfg.Template.is_public, self.cfg.Template.public)

    def test_is_owner(self):
        """Does it identify user?"""
        self.cfg.set_user(2)
        self.assertTrue(self.cfg.Template.is_owner(self.cfg.user), self.cfg.user)
        # This should be false
        self.cfg.set_user('default')
        self.assertFalse(self.cfg.Template.is_owner(self.cfg.user), self.cfg.user)



