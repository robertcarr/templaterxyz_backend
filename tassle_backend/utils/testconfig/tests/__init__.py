from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.files.base import ContentFile

from restapi.models import Templates
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

    def test_set_user(self):
        """Public Method for setting user"""
        self.obj.set_user('admin')
        self.assertEqual(self.obj.uid, self.obj.cfg['users']['admin']['pk'])


class TestConfigTemplates(TestCase):
    """
    Make sure we can access template & parameter content in the config
    """
    fixtures = ['default']

    def setUp(self):
        self.obj = TestConfig()

    def test_get_template(self):
        t = self.obj.template
        self.assertIsInstance(t['content'], ContentFile)

    def test_get_params(self):
        p = self.obj.params
        self.assertIsInstance(p['content'], ContentFile)

    def test_template_init(self):
        """Default template set"""
        self.assertIsInstance(self.obj.Template, Templates)

    def test_set_template(self):
        """Set to specific pk"""
        self.obj.set_template(2)
        self.assertEqual(self.obj.Template.pk, 2)