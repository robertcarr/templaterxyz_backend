from django.test import TestCase

from restapi.models import Templates
from utils.testconfig import TestConfig


class TestTemplates(TestCase):
    fixtures = ['default']

    def setUp(self):
        self.t = TestConfig()


