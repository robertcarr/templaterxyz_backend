import logging

from rest_framework.test import APIClient
from django.contrib.auth.models import AnonymousUser

log = logging.getLogger(__name__)


class APIAdvancedAuth(APIClient):
    """
    Add some additional functionality for authenticating with JWT tokens
    and existing User objects
    """
    TOKEN_FIELD = 'auth_token'
    TOKEN_TYPE = 'Token'

    def __init__(self, *args, **kwargs):
        super(APIAdvancedAuth, self).__init__(*args, **kwargs)

    def _get_user_token(self, user):
        """Get api token from a User object"""
        try:
            token = getattr(user, self.TOKEN_FIELD)
            return token.key
        except AttributeError:
            raise AttributeError(f'User missing API token {self.TOKEN_FIELD}')

    @property
    def current_user(self):
        return self._user

    @property
    def api_key(self):
        assert (self._user is not None), "User not set"
        return self._get_user_token(self._user)

    def _get_auth_header(self):
        """Return a dict with the client header to be added for authentication"""
        return {'HTTP_AUTHORIZATION': f'{self.TOKEN_TYPE} {self.api_key}'}

    def set_user(self, user=None):
        """set current user, api_key and credentials for API client"""
        log.debug(f'Setting API Client User={user}')
        if user:
            self._user = user
            self.credentials(**self._get_auth_header())
        else:
            self.logout()
            self._user = None
            self.credentials()


