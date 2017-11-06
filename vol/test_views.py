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


class ResultsViewTests(TransactionTestCase):
    def test_get_results_none(self):
        response = self.client.get('/results/Nonesense/Nonesense', secure=True)

        self.assertEqual(response.context[0]['total_job_count'], 0)
        self.assertEqual(response.context[0]['match_count'], 0)
        self.assertEqual(response.context[0]['interests_matches_count'], 0)
        self.assertEqual(response.context[0]['location_matches_count'], 0)
        self.assertEqual(response.status_code, 200)

    def test_get_results_one_complete_match(self):
        label = LabelsFactory(name="nature")
        job = JobFactory()
        job.labels.add(label.id)

        response = self.client.get('/results/wellington/nature', secure=True)

        self.assertEqual(response.context[0]['total_job_count'], 1)
        self.assertEqual(response.context[0]['match_count'], 1)
        self.assertEqual(response.context[0]['interests_matches_count'], 1)
        self.assertEqual(response.context[0]['location_matches_count'], 1)
        self.assertEqual(response.status_code, 200)

    def test_get_results_one_location_only(self):
        label = LabelsFactory()
        job = JobFactory()
        job.labels.add(label.id)

        response = self.client.get('/results/wellington/Nature', secure=True)

        self.assertEqual(response.context[0]['total_job_count'], 1)
        self.assertEqual(response.context[0]['match_count'], 1)
        self.assertEqual(response.context[0]['interests_matches_count'], 0)
        self.assertEqual(response.context[0]['location_matches_count'], 1)
        self.assertEqual(response.status_code, 200)

    def test_get_results_one_label_only(self):
        label = LabelsFactory(name="nature")
        job = JobFactory(city="Dunedin")
        job.labels.add(label.id)

        response = self.client.get('/results/wellington/nature', secure=True)

        self.assertEqual(response.context[0]['total_job_count'], 1)
        self.assertEqual(response.context[0]['match_count'], 0)
        self.assertEqual(response.context[0]['interests_matches_count'], 1)
        self.assertEqual(response.context[0]['location_matches_count'], 0)
        self.assertEqual(response.status_code, 200)

    def test_get_results_many(self):
        label = LabelsFactory(name="nature")
        job_one = JobFactory()
        job_one.labels.add(label.id)
        job_two = JobFactory(title="Butterfly catcher",
                             url="http://www.example.com/")
        job_two.labels.add(label.id)

        response = self.client.get('/results/wellington/nature', secure=True)

        self.assertEqual(response.context[0]['total_job_count'], 2)
        self.assertEqual(response.context[0]['match_count'], 2)
        self.assertEqual(response.context[0]['interests_matches_count'], 2)
        self.assertEqual(response.context[0]['location_matches_count'], 2)
        self.assertEqual(response.status_code, 200)

    def test_get_results_many_complete_match(self):
        label = LabelsFactory(name="nature")
        job_one = JobFactory()
        job_one.labels.add(label.id)
        job_two = JobFactory(title="Butterfly catcher",
                             url="http://www.example.com/")
        job_two.labels.add(label.id)

        response = self.client.get('/results/wellington/nature', secure=True)

        self.assertEqual(response.context[0]['total_job_count'], 2)
        self.assertEqual(response.context[0]['match_count'], 2)
        self.assertEqual(response.context[0]['interests_matches_count'], 2)
        self.assertEqual(response.context[0]['location_matches_count'], 2)
        self.assertEqual(response.status_code, 200)

    def test_get_results_many_location_only(self):
        JobFactory()
        JobFactory(title="Butterfly catcher",
                   url="http://www.example.com/")

        response = self.client.get('/results/wellington/nature', secure=True)

        self.assertEqual(response.context[0]['total_job_count'], 2)
        self.assertEqual(response.context[0]['match_count'], 2)
        self.assertEqual(response.context[0]['interests_matches_count'], 0)
        self.assertEqual(response.context[0]['location_matches_count'], 2)
        self.assertEqual(response.status_code, 200)

    def test_get_results_many_label_only(self):
        label = LabelsFactory(name="nature")
        job_one = JobFactory(city="Dunedin")
        job_one.labels.add(label.id)
        job_two = JobFactory(title="Butterfly catcher",
                             city="Amsterdam")
        job_two.labels.add(label.id)

        response = self.client.get('/results/wellington/nature', secure=True)

        self.assertEqual(response.context[0]['total_job_count'], 2)
        self.assertEqual(response.context[0]['match_count'], 0)
        self.assertEqual(response.context[0]['interests_matches_count'], 2)
        self.assertEqual(response.context[0]['location_matches_count'], 0)
        self.assertEqual(response.status_code, 200)


class JobViewTests(TransactionTestCase):
    def test_get_job_none(self):
        response = self.client.get('/jobs/028b7d48-3691-459e-93c3-5cd147a92dfd', secure=True)
        self.assertEqual(response.status_code, 404)

    def test_get_job_one(self):
        job = JobFactory()
        response = self.client.get('/jobs/{}'.format(job.slug), secure=True)
        self.assertEqual(response.context[0]['job'], job)
