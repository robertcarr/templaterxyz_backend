from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from utils.testconfig import TestConfig



class TestConfigClass(TestCase):
    fixtures = ['default']

    def setUp(self):
        self.obj = TestConfig()

    def test__set_user_anonymous(self):
        """Anon User"""
        self.obj._set_user()
        self.assertEqual(self.obj.user, AnonymousUser)

    def test__set_user_by_uid(self):
        """Set user by User ID/PK"""
        self.obj._set_user(1)
        self.assertEqual(self.obj.user.pk, 1)
        self.assertEqual(self.obj.uid, 1)

    def test__set_user_by_role(self):
        """Set user by Role"""
        self.obj._set_user('admin')
        self.assertEqual(self.obj.user, self.obj.User.objects.get(pk=self.obj.cfg['users']['admin']['pk']))

    def test__set_user_additional_cfg(self):
        """Does the Users object have an additional dict of data?"""
        self.obj._set_user('admin')
        self.assertEqual(self.obj.settings, self.obj.cfg['users']['admin'])

    def test__set_user_additional_cfg_default_none(self):
        """settings set to None for no user"""
        self.assertIsNone(self.obj.settings)