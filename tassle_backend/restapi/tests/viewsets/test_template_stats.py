from rest_framework.test import APITestCase
from django.urls import reverse

from utils.drf import APIAdvancedAuth


class TestStats(APITestCase):
    """
    Check basic stats work for things needed on the homepage, etc
    """
    fixtures = ['default']

    def setUp(self):
        self.client = APIAdvancedAuth()

    def test_get_template_stats(self):
        resp = self.client.get(reverse('stats-list'), format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('templates_rendered' in resp.data, resp.data)
