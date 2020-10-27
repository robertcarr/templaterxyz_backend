"""
Common/Useful Configuration Parameters for Unittests
"""
import json

from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser


class TestConfig:
    """
    Easier Config Handling.

    init(user=[<key>|<id>]
    """
    cfg = {
        'users': {
            'admin': {'pk': 1},
            'default': {'pk': 1}
        }
    }

    def __init__(self, *args, **kwargs):
        self.User = get_user_model()
        self.uid = None
        self.user = AnonymousUser
        self.settings = None

    def _set_user(self, user=None):
        """Set the current user, default to Anon"""
        uid = None
        try:
            uid = getattr(self, 'cfg')['users'][user]['pk']
            self.settings = self.cfg['users'][user]
        except (TypeError, KeyError):
            if isinstance(user, int):
                uid = user
        if uid:
            self.uid = uid
            self.user = self.User.objects.get(pk=uid)



