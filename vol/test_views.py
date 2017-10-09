from django.core.urlresolvers import reverse
from django.test import TestCase

# TODO: add same redirect test, and think of other things that make sense to test
class IndexViewTests(TestCase):
    # pass
    def test_index_view(self):
        response = self.client.get(reverse('index'), secure=True)
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "foo")
        # self.assertQuerysetEqual(response.context['categories'], [])