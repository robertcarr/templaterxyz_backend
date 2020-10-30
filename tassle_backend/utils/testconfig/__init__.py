"""
Common/Useful Configuration Parameters for Unittests
"""
import json
from functools import reduce

from jinja2 import Template as JinjaTemplate

from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from restapi.models import Templates

class TestConfig:
    """
    Easier Config Handling.

    init(user=[<key>|<id>]


    """
    cfg = {
        't': 'my name is {{ name }}',
        'p': '{"name": "joe"}',
        'template': {'pk': 1,
                     'uuid': 'egLRvtJEMhSeDJKjsuEBxG',
                     'file': {'name': 'test.t2',
                              'content': ContentFile('''My name is {{ name }}''')
                              }},
        'params': {'file': {'name': 'params.json',
                            'content': ContentFile(json.dumps(dict({'name': 'test_user'})))
                            }},
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
        self.set_template()
        self._Templates = Templates

    @property
    def template(self):
        return self.cfg['template']['file']

    @property
    def params(self):
        return self.cfg['params']['file']

    def get_template_file(self):
        """Return file for testing"""
        f = ContentFile(self.cfg['t'])
        f.name = 'test.t2'
        return f

    def get_params_file(self):
        """ return param file for testing"""
        f = ContentFile(self.cfg['p'])
        f.name = 'params.json'
        return f

    def set_template(self, pk=None):
        """Set the active template to use, set to default cfg if not supplied"""
        if not pk:
            pk = self.cfg['template']['pk']
        self.Template = Templates.objects.get(pk=pk)

    @property
    def fake_render(self):
        """return Jinja2 Rendered from cfg values"""
        t = JinjaTemplate(self.cfg['t']).render(json.loads(self.cfg['p']))
        return t

    def set_user(self, user=None):
        self._set_user(user)

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

