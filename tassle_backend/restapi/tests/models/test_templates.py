from django.test import TestCase

from restapi import models


class TestTemplates(TestCase):
    fixtures = ['default']

    def setUp(self):
        self.obj = models.Templates.get(pk=1)

