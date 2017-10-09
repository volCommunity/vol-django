from django.core.urlresolvers import reverse
from django.test import TestCase


class IndexViewTests(TestCase):
    # Assert we are redirected to a secure url
    def test_index_insecure_redirects(self):
        response = self.client.get(reverse('index'), secure=False)
        self.assertEqual(response.status_code, 301)

    def test_index_view(self):
        response = self.client.get(reverse('index'), secure=True)
        self.assertEqual(response.status_code, 200)
