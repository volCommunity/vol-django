from django.core.urlresolvers import reverse
from django.test import TransactionTestCase

from vol.factories import LabelsFactory, JobFactory


class IndexViewTests(TransactionTestCase):
    # Assert we are redirected to a secure url
    def test_index_insecure_redirects(self):
        response = self.client.get(reverse('index'), secure=False)
        self.assertEqual(response.status_code, 301)

    def test_index_view(self):
        response = self.client.get(reverse('index'), secure=True)
        self.assertEqual(response.status_code, 200)

    def test_get_results_none(self):
        response = self.client.get('/results/Nonesense/Nonesense', secure=True)

        self.assertEqual(response.context[0]['job_count'], 0)
        self.assertEqual(response.context[0]['matched_intersection'], 0)
        self.assertEqual(response.context[0]['matched_interests_count'], 0)
        self.assertEqual(response.context[0]['location_matches'], 0)
        self.assertEqual(response.status_code, 200)

    def test_get_results_one_complete_match(self):
        label = LabelsFactory(name="nature")
        job = JobFactory()
        job.labels.add(label.id)

        response = self.client.get('/results/wellington/nature', secure=True)

        self.assertEqual(response.context[0]['job_count'], 1)
        self.assertEqual(response.context[0]['matched_intersection'], 1)
        self.assertEqual(response.context[0]['matched_interests_count'], 1)
        self.assertEqual(response.context[0]['location_matches'], 1)
        self.assertEqual(response.status_code, 200)

    def test_get_results_one_location_only(self):
        label = LabelsFactory()
        job = JobFactory()
        job.labels.add(label.id)

        response = self.client.get('/results/wellington/Nature', secure=True)

        self.assertEqual(response.context[0]['job_count'], 1)
        self.assertEqual(response.context[0]['matched_intersection'], 0)
        self.assertEqual(response.context[0]['matched_interests_count'], 0)
        self.assertEqual(response.context[0]['location_matches'], 1)
        self.assertEqual(response.status_code, 200)

    def test_get_results_one_label_only(self):
        label = LabelsFactory(name="nature")
        job = JobFactory(city="Dunedin")
        job.labels.add(label.id)

        response = self.client.get('/results/wellington/nature', secure=True)

        self.assertEqual(response.context[0]['job_count'], 1)
        self.assertEqual(response.context[0]['matched_intersection'], 0)
        self.assertEqual(response.context[0]['matched_interests_count'], 1)
        self.assertEqual(response.context[0]['location_matches'], 0)
        self.assertEqual(response.status_code, 200)

    def test_get_results_many(self):
        label = LabelsFactory(name="nature")
        job_one = JobFactory()
        job_one.labels.add(label.id)
        job_two = JobFactory(title="Butterfly catcher",
                             url="http://www.example.com/")
        job_two.labels.add(label.id)

        response = self.client.get('/results/wellington/nature', secure=True)

        self.assertEqual(response.context[0]['job_count'], 2)
        self.assertEqual(response.context[0]['matched_intersection'], 2)
        self.assertEqual(response.context[0]['matched_interests_count'], 1)
        self.assertEqual(response.context[0]['location_matches'], 2)
        self.assertEqual(response.status_code, 200)

    def test_get_results_many_complete_match(self):
        label = LabelsFactory(name="nature")
        job_one = JobFactory()
        job_one.labels.add(label.id)
        job_two = JobFactory(title="Butterfly catcher",
                             url="http://www.example.com/")
        job_two.labels.add(label.id)

        response = self.client.get('/results/wellington/nature', secure=True)

        self.assertEqual(response.context[0]['job_count'], 2)
        self.assertEqual(response.context[0]['matched_intersection'], 2)
        self.assertEqual(response.context[0]['matched_interests_count'], 1)
        self.assertEqual(response.context[0]['location_matches'], 2)
        self.assertEqual(response.status_code, 200)

    def test_get_results_many_location_only(self):
        JobFactory()
        JobFactory(title="Butterfly catcher",
                   url="http://www.example.com/")

        response = self.client.get('/results/wellington/nature', secure=True)

        self.assertEqual(response.context[0]['job_count'], 2)
        self.assertEqual(response.context[0]['matched_intersection'], 0)
        self.assertEqual(response.context[0]['matched_interests_count'], 0)
        self.assertEqual(response.context[0]['location_matches'], 2)
        self.assertEqual(response.status_code, 200)

    def test_get_results_many_label_only(self):
        label = LabelsFactory(name="nature")
        job_one = JobFactory(city="Dunedin")
        job_one.labels.add(label.id)
        job_two = JobFactory(title="Butterfly catcher",
                             city="Amsterdam")
        job_two.labels.add(label.id)

        response = self.client.get('/results/wellington/nature', secure=True)

        self.assertEqual(response.context[0]['job_count'], 2)
        self.assertEqual(response.context[0]['matched_intersection'], 0)
        self.assertEqual(response.context[0]['matched_interests_count'], 1)
        self.assertEqual(response.context[0]['location_matches'], 0)
        self.assertEqual(response.status_code, 200)
