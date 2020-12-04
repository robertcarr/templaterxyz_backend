import json
from unittest import skip

from django.conf import settings
from django.test import TestCase, RequestFactory
from rest_framework.test import APIRequestFactory
from unittest import skip
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from utils.drf import APIAdvancedAuth

User = get_user_model()

class TestAPIAuth(TestCase):
    fixtures = ['default']

    def setUp(self):
        self.obj = APIAdvancedAuth()
        self.user = User.objects.get(pk=1)
        self.obj.set_user(self.user)

    def test_set_user(self):
        """Set a User"""
        self.assertEqual(self.obj._user, self.user)
        self.assertEqual(self.obj.api_key, self.user.auth_token.key)

    def test__get_auth_header(self):
        """Do we return proper dict for Auth header?"""
        header = self.obj._get_auth_header()
        self.assertIsInstance(header, dict)
        self.assertEqual(header['HTTP_AUTHORIZATION'],
                         f'{self.obj.TOKEN_TYPE} {self.obj.api_key}')

    def test__get_user_token(self):
        """ Retrieve user token"""
        token = self.obj._get_user_token(self.user)
        self.assertEqual(token, getattr(self.user, self.obj.TOKEN_FIELD).key)

    def test__get_user_token_fails(self):
        """We should assert AttributeError if field doesn't exist"""
        self.obj.TOKEN_FIELD = 'does_not_exist'
        with self.assertRaises(AttributeError) as e:
            self.obj._get_user_token(self.user)

    def test_get_request(self):
        """Can we perform basic client non-auth operations as User"""
        resp = self.obj.get('/')
        self.assertEqual(json.loads(resp.content)['status'], 'ok')

    @skip('Auth disabled for now')
    def test_get_request_no_auth(self):
        """Do we get denied without USER set/Anonymous set?"""
        self.obj.set_user()
        resp = self.obj.get('/api/')
        self.assertEqual(resp.status_code, 401)

    def test_current_user(self):
        """Is the current user set?"""
        user = self.obj.current_user
        self.assertEqual(user.pk, 1)

    def test_current_user_anon(self):
        """Anonymous user?"""
        self.obj.set_user()
        user = self.obj.current_user
        self.assertIsNone(user)

    def test_get_api_get_no_user(self):
        """Do we choke when no user set?"""
        self.obj.set_user()
        with self.assertRaises(AssertionError) as e:
            self.obj.api_key

    def test_auth_request(self):
        """Check API Token that requires AUTH to make sure we set header correctly"""
        self.obj.set_user(self.user)
        resp = self.obj.get('/api/')
        self.assertEqual(resp.status_code, 200, resp.content)


class TestRequestFactory(TestCase):
    """We include RequestFactory Instance() in the object"""
    fixtures = ['default']

    def setUp(self):
        self.obj = APIAdvancedAuth()
        self.user = User.objects.get(pk=1)

    def test_has_factory(self):
        self.assertIsInstance(self.obj.factory, APIRequestFactory)

    def test_init_is_anonymous(self):
        self.assertEqual(self.obj.factory.user, AnonymousUser())

    def test_set_user_sets_factory_user(self):
        """Do we set obj.factory.user correctly?"""
        self.obj.set_user(self.user)
        self.assertEqual(self.obj.factory.user, self.user)

    def test_unset_user_to_anonymous(self):
        self.obj.set_user() # unset user
        self.assertEqual(self.obj.factory.user, AnonymousUser())
