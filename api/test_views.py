import json

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from vol.factories import LabelsFactory, OrganisationFactory, SiteFactory, JobFactory
from vol.models import Labels, Site, Job

""" Create tests for:
 get, create (verify only auth), update (verify only auth), delete (verify only auth)
"""


class IndexViewTests(APITestCase):
    def setUp(self):
        self.base_url = "/api"
        # TODO: don't be lazy and create roles too, and use a less privileged user
        user = User.objects.create_superuser('admin', 'admin@example.com', 'test123')
        self.token = Token.objects.create(user=user)

        self.job_json = {"title": "Eternal Gardener",
                         "text": "for the nature lover",
                         "country": "NZ",
                         "region": "Wellington",
                         "city": "Wellington",
                         "url": "http://www.example.com/jobs/2",
                         "seen": 0}

        self.organisation_json = {
            "name": "The nappy changers",
            "description": "We change nappies",
            "country": "New Zealand",
            "city": "Wellington",
            "region": "Wellington",
            "url": "www.example.com/organisations/nappychangers"
        }

        self.label_json = {
            "name": "Gardens"
        }

        self.site_json = {
            "name": "A site",
            "url": "localhost"
        }

    # Assert we are redirected to a secure url
    def test_index_insecure_redirects(self):
        response = self.client.get('/api', secure=False)
        self.assertEqual(response.status_code, 301)

    # Assert that we will be redirect to "/api" if we hit "/api"
    def test_index_view(self):
        response = self.client.get('/api', secure=True)
        self.assertEqual(response.status_code, 302)

    def test_index_view_trailing(self):
        response = self.client.get('/api/', secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "labels")

    """ Labels CRUD
        Create """

    def test_create_label_auth(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.post('%s/labels' % self.base_url, {'name': 'nature'}, format='json', secure=True)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Labels.objects.count(), 1)
        self.assertEqual(Labels.objects.get(name="nature").name, 'nature')
        r = json.loads(response.content)
        self.assertEqual(r['name'], "nature")

    def test_create_label_requires_authentications(self):
        client = APIClient()
        response = client.post('%s/labels' % self.base_url, {'name': 'nature'}, format='json', secure=True)
        self.assertEqual(response.status_code, 401)

    """ Read """

    def test_get_labels_one(self):
        label = LabelsFactory()
        client = APIClient()
        response = client.get('%s/labels/%s' % (self.base_url, label.uuid), format='json',
                              secure=True)
        r = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(r['name'], label.name)

    def test_get_labels_many(self):
        LabelsFactory()  # TODO: refactor label factory to take number
        LabelsFactory(name="nature")
        client = APIClient()
        response = client.get('%s/labels' % (self.base_url), format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(r['count'], 2)

    def test_get_labels__four_oh_fours(self):
        client = APIClient()
        response = client.get('%s/labels/%s' % (self.base_url, 999), format='json', secure=True)
        self.assertEqual(response.status_code, 404)

    def test_get_labels_none(self):
        client = APIClient()
        response = client.get('%s/labels' % self.base_url, format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(r['count'], 0)

    """ Update """

    def test_update_labels(self):
        label = LabelsFactory()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {'name': 'clowns'}
        response = client.put('%s/labels/%s' % (self.base_url, label.uuid), data=data,
                              format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(r['name'], "clowns")

    def test_update_labels_four_oh_fours(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.put('%s/labels/%s' % (self.base_url, 999), {'name': 'nature'}, format='json', secure=True)
        self.assertEqual(response.status_code, 404)

    def test_update_labels_requires_authentications(self):
        label = LabelsFactory()
        client = APIClient()
        response = client.put('%s/labels/%s' % (self.base_url, label.uuid),
                              {'name': 'nature'}, format='json', secure=True)
        self.assertEqual(response.status_code, 401)

    """ Delete """

    def test_delete_labels(self):
        label = LabelsFactory()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.delete('%s/labels/%s' % (self.base_url, label.uuid), format='json',
                                 secure=True)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Labels.objects.count(), 0)

    def test_delete_labels_requires_authentications(self):
        label = LabelsFactory()
        client = APIClient()
        response = client.delete('%s/labels/%s' % (self.base_url, label.uuid), format='json',
                                 secure=True)
        self.assertEqual(response.status_code, 401)

    def test_delete_labels_four_oh_fours(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.delete('%s/labels/%s' % (self.base_url, 999), format='json', secure=True)
        self.assertEqual(response.status_code, 404)

    """ Organisation CRUD
        Create """

    def test_create_organisation(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.post('%s/organisations' % self.base_url, self.organisation_json, format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(r['name'], "The nappy changers")
        self.assertEqual(r['url'], "www.example.com/organisations/nappychangers")

    def test_create_organisation_requires_authentication(self):
        client = APIClient()
        response = client.post('%s/organisations' % self.base_url, self.organisation_json, format='json', secure=True)
        self.assertEqual(response.status_code, 401)

    """ Read """

    def test_get_organisation_one(self):
        organisation = OrganisationFactory()
        client = APIClient()
        response = client.get(
            '%s/organisations/%s' % (self.base_url, organisation.uuid),
            format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(r['name'], organisation.name)

    def test_get_organisation_many(self):
        OrganisationFactory()  # TODO: refactor to create n orgs
        OrganisationFactory(name="Another Organisation")
        client = APIClient()
        response = client.get('%s/organisations' % self.base_url, format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(r['count'], 2)

    def test_get_organisation_four_oh_fours(self):
        client = APIClient()
        response = client.get('%s/sites/%s' % (self.base_url, 999), format='json', secure=True)
        self.assertEqual(response.status_code, 404)

    def test_get_organisation_none(self):
        client = APIClient()
        response = client.get('%s/organisations' % self.base_url, format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(r['count'], 0)

    """ Update """

    def test_update_organisation(self):
        organisation = OrganisationFactory()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = self.organisation_json
        data["name"] = "The body snatchers"
        response = client.put(
            '%s/organisations/%s' % (self.base_url, organisation.uuid), data=data,
            format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(r['name'], "The body snatchers")

    def test_update_organisation_four_oh_fours(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.put('%s/organisations/%s' % (self.base_url, 999), self.organisation_json, format='json',
                              secure=True)
        self.assertEqual(response.status_code, 404)

    def test_update_organisation_requires_authentication(self):
        organisation = OrganisationFactory()
        client = APIClient()
        response = client.put(
            '%s/organisations/%s' % (self.base_url, organisation.uuid),
            self.organisation_json, format='json', secure=True)
        self.assertEqual(response.status_code, 401)

    """ Delete """

    def test_delete_organisation(self):
        organisation = OrganisationFactory()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.delete(
            '%s/organisations/%s' % (self.base_url, organisation.uuid),
            format='json', secure=True)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Site.objects.count(), 0)

    def test_delete_organisation_requires_authentications(self):
        organisation = OrganisationFactory()
        client = APIClient()
        response = client.delete(
            '%s/organisations/%s' % (self.base_url, organisation.uuid),
            format='json', secure=True)
        self.assertEqual(response.status_code, 401)

    def test_delete_organisation_four_oh_fours(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.delete('%s/organisations/%s' % (self.base_url, 999), format='json', secure=True)
        self.assertEqual(response.status_code, 404)

    """ Sites CRUD
        Create """

    def test_create_site(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.post('%s/sites' % self.base_url,
                               {'name': 'Do Gooders', 'url': 'www.example.com/dogooders/jobs'}, format='json',
                               secure=True)
        self.assertEqual(Site.objects.count(), 1)
        self.assertEqual(Site.objects.get(name="Do Gooders").name, 'Do Gooders')
        r = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(r['name'], "Do Gooders")
        self.assertEqual(r['url'], "www.example.com/dogooders/jobs")

    def test_create_site_requires_authentications(self):
        client = APIClient()
        response = client.post('%s/sites' % self.base_url,
                               {'name': 'Do Gooders', 'url': 'www.example.com/dogooders/jobs'}, format='json',
                               secure=True)
        self.assertEqual(response.status_code, 401)

    """ Read """

    def test_get_sites_one(self):
        site = SiteFactory()
        client = APIClient()
        response = client.get('%s/sites/%s' % (self.base_url, site.uuid), format='json',
                              secure=True)
        r = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(r['name'], site.name)

    def test_get_sites_many(self):
        SiteFactory()
        SiteFactory(name="Another Site")
        client = APIClient()
        response = client.get('%s/sites' % self.base_url, format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(r['count'], 2)

    def test_get_site_four_oh_fours(self):
        client = APIClient()
        response = client.get('%s/sites/%s' % (self.base_url, 999), format='json', secure=True)
        self.assertEqual(response.status_code, 404)

    def test_get_sites_none(self):
        client = APIClient()
        response = client.get('%s/sites' % self.base_url, format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(r['count'], 0)

    """ Update """

    def test_update_sites(self):
        site = SiteFactory()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {'name': 'Clowns for Justice', 'url': 'www.example.com/dogooders/jobs'}
        response = client.put('%s/sites/%s' % (self.base_url, site.uuid), data=data,
                              format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(r['name'], "Clowns for Justice")

    def test_update_sites_four_oh_fours(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.put('%s/sites/%s' % (self.base_url, 999),
                              {'name': 'Do Gooders', 'url': 'www.example.com/dogooders/jobs'}, format='json',
                              secure=True)
        self.assertEqual(response.status_code, 404)

    def test_update_sites_requires_authentications(self):
        site = SiteFactory()
        client = APIClient()
        response = client.put('%s/sites/%s' % (self.base_url, site.uuid),
                              {'name': 'Do Gooders', 'url': 'www.example.com/dogooders/jobs'}, format='json',
                              secure=True)
        self.assertEqual(response.status_code, 401)

    """ Delete """

    def test_delete_site(self):
        site = SiteFactory()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.delete('%s/sites/%s' % (self.base_url, site.uuid), format='json',
                                 secure=True)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Site.objects.count(), 0)

    def test_delete_site_requires_authentications(self):
        site = SiteFactory()
        client = APIClient()
        response = client.delete('%s/sites/%s' % (self.base_url, site.uuid), format='json',
                                 secure=True)
        self.assertEqual(response.status_code, 401)

    def test_delete_site_four_oh_fours(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.delete('%s/sites/%s' % (self.base_url, 999), format='json', secure=True)
        self.assertEqual(response.status_code, 404)

    """ Jobs CRUD
        Create """

    def test_create_job_auth(self):
        # TODO: DRY, see test_update_jobs
        data = self.job_json
        data['labels'] = [self.label_json]
        data['sites'] = [self.site_json]
        data['organisation'] = self.organisation_json

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        response = client.post('%s/jobs' % self.base_url, data=data, format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(r['title'], "Eternal Gardener")
        self.assertEqual(r['text'], "for the nature lover")
        self.assertEqual(r['sites'][0]['name'], data['sites'][0]['name'])
        self.assertEqual(r['labels'][0]['name'], data['labels'][0]['name'])

    def test_create_jobs_conflicting_site_validation_error(self):
        # TODO: DRY, see test_update_jobs
        site = SiteFactory()

        data = self.job_json
        data['labels'] = [self.label_json]
        data['sites'] = [{'name': "Different name than the prexisting site",
                          'url': site.url}]
        data['organisation'] = self.organisation_json

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        response = client.post('%s/jobs' % self.base_url, data=data, format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(r[0], "Site failed to pass validation: different site with identical name found")

    def test_create_jobs_organisation_empty_description_ok(self):
        # TODO: DRY, see test_update_jobs
        data = self.job_json
        data['labels'] = [self.label_json]
        data['sites'] = [self.site_json]

        data['organisation'] = {'name': "An org",
                                'description': "",
                                'city': "A city",
                                'region': "A region",
                                'country': "A country",
                                'url': "A URL"}

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        response = client.post('%s/jobs' % self.base_url, data=data, format='json', secure=True)
        self.assertEqual(response.status_code, 201)

    def test_create_jobs_organisation_not_required(self):
        # TODO: DRY, see test_update_jobs
        data = self.job_json
        data['labels'] = [self.label_json]
        data['sites'] = [self.site_json]

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        response = client.post('%s/jobs' % self.base_url, data=data, format='json', secure=True)
        self.assertEqual(response.status_code, 201)

    def test_create_jobs_conflicting_organisation_validation_error(self):
        # TODO: DRY, see test_update_jobs
        organisation = OrganisationFactory()

        data = self.job_json
        data['labels'] = [self.label_json]
        data['sites'] = [self.site_json]

        data['organisation'] = {'name': organisation.name,
                                'description': organisation.description,
                                'city': organisation.city,
                                'region': organisation.region,
                                'country': "UK",
                                'url': organisation.url}

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        response = client.post('%s/jobs' % self.base_url, data=data, format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(r[0],
                         "Organisation failed to pass validation: organisation with the same name but " +
                         "different country found (NZ vs UK)")

    def test_create_job_no_auth(self):
        client = APIClient()
        response = client.post('%s/labels' % self.base_url, self.job_json, format='json', secure=True)
        self.assertEqual(response.status_code, 401)

        """ Read """

    def test_get_jobs_one(self):
        job = JobFactory.create()
        client = APIClient()
        response = client.get('%s/jobs/%s' % (self.base_url, job.uuid), format='json',
                              secure=True)
        r = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(r['title'], job.title)

    def test_get_jobs_many(self):
        JobFactory.create()
        JobFactory.create(title="Trail builder")
        client = APIClient()
        response = client.get('%s/jobs' % (self.base_url), format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(r['count'], 2)

    def test_get_jobs_none(self):
        client = APIClient()
        response = client.get('%s/jobs' % (self.base_url), format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(r['count'], 0)

    def test_get_jobs_four_oh_fours(self):
        client = APIClient()
        response = client.get('%s/jobs/%s' % (self.base_url, 999), format='json', secure=True)
        self.assertEqual(response.status_code, 404)

    """ Update """

    def test_update_jobs(self):
        job = JobFactory.create()

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = self.job_json
        data["title"] = "Clown"

        response = client.patch('%s/jobs/%s' % (self.base_url, job.uuid), data=data,
                                format='json', secure=True)

        r = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(r['title'], "Clown")

    def test_update_jobs_organisation(self):
        """
        Verify that if the org in the update request is different, but does not raise a
        conflict error, a new org is created and linked.
        :return:
        """
        job = JobFactory.create()

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = self.job_json
        data['organisation'] = {'name': "A new name"}

        response = client.patch('%s/jobs/%s' % (self.base_url, job.uuid), data=data,
                                format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(r['organisation']['uuid'], str(job.organisation.uuid))
        self.assertEqual(r['organisation']['name'], "A new name")

    def test_update_jobs_organisation_validation_error(self):
        organisation = OrganisationFactory()

        label = LabelsFactory()
        site = SiteFactory()
        job = JobFactory.create()

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = self.job_json
        data['labels'] = [{'name': label.name}]
        data['sites'] = [{'name': site.name,
                          'url': site.url}]
        data['organisation'] = {'name': organisation.name,
                                'description': organisation.description,
                                'city': organisation.city,
                                'region': organisation.region,
                                'country': "UK",
                                'url': organisation.url}

        response = client.put('%s/jobs/%s' % (self.base_url, job.uuid), data=data,
                              format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(r[0],
                         "Organisation failed to pass validation: organisation with the same name but " +
                         "different country found (NZ vs UK)")

    def test_update_jobs_labels(self):
        label = LabelsFactory()
        job = JobFactory.create()

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = self.job_json
        data['labels'] = [{'name': label.name},
                          {'name': "a new label"}]

        response = client.patch('%s/jobs/%s' % (self.base_url, job.uuid), data=data,
                                format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(r['labels']), 2)

    def test_update_jobs_sites(self):
        site = SiteFactory()

        job = JobFactory.create()

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = self.job_json
        data['sites'] = [{'name': site.name,
                          'url': site.url},
                         {'name': 'a new site',
                          'url': '127.0.0.0'}]

        response = client.patch('%s/jobs/%s' % (self.base_url, job.uuid), data=data,
                                format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(r['sites']), 2)

    def test_update_jobs_sites_should_validation_error(self):
        site = SiteFactory()

        label = LabelsFactory()
        job = JobFactory.create()

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = self.job_json
        data['labels'] = [{'name': label.name}]
        data['sites'] = [{'name': "Should raise a validation error",
                          'url': site.url}]
        data['organisation'] = {'name': job.organisation.name,
                                'description': job.organisation.description,
                                'city': job.organisation.city,
                                'region': job.organisation.region,
                                'country': job.organisation.country,
                                'url': job.organisation.url}

        response = client.put('%s/jobs/%s' % (self.base_url, job.uuid), data=data,
                              format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(r[0], "Site failed to pass validation: different site with identical name found")

    def test_update_jobs_four_oh_fours(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.put('%s/jobs/%s' % (self.base_url, 999), self.job_json, format='json', secure=True)
        self.assertEqual(response.status_code, 404)

    def test_update_jobs_requires_authentications(self):
        job = JobFactory.create()
        client = APIClient()
        data = self.job_json
        response = client.put('%s/jobs/%s' % (self.base_url, job.uuid), data=data,
                              format='json', secure=True)
        self.assertEqual(response.status_code, 401)

    """ Delete """

    def test_delete_jobs(self):
        job = JobFactory.create()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        length = Job.objects.count()
        response = client.delete('%s/jobs/%s' % (self.base_url, job.uuid),
                                 format='json', secure=True)
        length -= 1
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Job.objects.count(), length)

    def test_delete_jobs_requires_authentications(self):
        job = JobFactory.create()
        client = APIClient()
        response = client.delete('%s/jobs/%s' % (self.base_url, job.uuid),
                                 format='json', secure=True)
        self.assertEqual(response.status_code, 401)

    def test_delete_jobs_four_oh_fours(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.delete('%s/jobs/%s' % (self.base_url, 999), format='json', secure=True)
        self.assertEqual(response.status_code, 404)
