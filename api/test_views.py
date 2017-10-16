import json

from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from vol.factories import LabelsFactory, OrganisationFactory, SiteFactory, JobFactory
from vol.models import Labels, Organisation, Site, Job

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
            "country": "New Zealand",
            "city": "Wellington",
            "region": "Wellington",
            "url": "www.example.com/organisations/nappychangers"
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
        length = Labels.objects.count()
        response = client.post('%s/labels' % self.base_url, {'name': 'nature'}, format='json', secure=True)
        length += 1
        self.assertEqual(Labels.objects.count(), length)
        self.assertEqual(Labels.objects.get(name="nature").name, 'nature')
        r = json.loads(response.content)
        self.assertEqual(r['name'], "nature")
        self.assertEqual(response.status_code, 201)

    def test_create_label_requires_authentications(self):
        client = APIClient()
        response = client.post('%s/labels' % self.base_url, {'name': 'nature'}, format='json', secure=True)
        self.assertEqual(response.status_code, 401)

    """ Read """

    def test_get_labels_one(self):
        LabelsFactory()
        client = APIClient()
        response = client.get('%s/labels/%s' % (self.base_url, Labels.objects.get(name="people").id), format='json',
                              secure=True)
        r = json.loads(response.content)
        self.assertEqual(r['name'], "people")
        self.assertEqual(response.status_code, 200)

    def test_get_labels_many(self):
        LabelsFactory()  # TODO: refactor label factory to take number
        LabelsFactory(name="nature")
        client = APIClient()
        response = client.get('%s/labels' % (self.base_url), format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(r['count'], 2)
        self.assertEqual(response.status_code, 200)

    def test_get_labels__four_oh_fours(self):
        client = APIClient()
        response = client.get('%s/labels/%s' % (self.base_url, 999), format='json', secure=True)
        self.assertEqual(response.status_code, 404)

    def test_get_labels_none(self):
        client = APIClient()
        response = client.get('%s/labels' % self.base_url, format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(r['count'], 0)
        self.assertEqual(response.status_code, 200)

    """ Update """

    def test_update_labels(self):
        LabelsFactory()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {'name': 'clowns'}
        response = client.put('%s/labels/%s' % (self.base_url, Labels.objects.get(name="people").id), data=data,
                              format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(r['name'], "clowns")
        self.assertEqual(response.status_code, 200)

    def test_update_labels_four_oh_fours(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.put('%s/labels/%s' % (self.base_url, 999), {'name': 'nature'}, format='json', secure=True)
        self.assertEqual(response.status_code, 404)

    def test_update_labels_requires_authentications(self):
        LabelsFactory()
        client = APIClient()
        response = client.put('%s/labels/%s' % (self.base_url, Labels.objects.get(name="people").id),
                              {'name': 'nature'}, format='json', secure=True)
        self.assertEqual(response.status_code, 401)

    """ Delete """

    def test_delete_labels(self):
        LabelsFactory()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.delete('%s/labels/%s' % (self.base_url, Labels.objects.get(name="people").id), format='json',
                                 secure=True)
        self.assertEqual(Labels.objects.count(), 0)
        self.assertEqual(response.status_code, 204)

    def test_delete_labels_requires_authentications(self):
        LabelsFactory()
        client = APIClient()
        response = client.delete('%s/labels/%s' % (self.base_url, Labels.objects.get(name="people").id), format='json',
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
        self.assertEqual(r['name'], "The nappy changers")
        self.assertEqual(r['url'], "www.example.com/organisations/nappychangers")
        self.assertEqual(response.status_code, 201)

    def test_create_organisation_requires_authentication(self):
        client = APIClient()
        response = client.post('%s/organisations' % self.base_url, self.organisation_json, format='json', secure=True)
        self.assertEqual(response.status_code, 401)

    """ Read """

    def test_get_organisation_one(self):
        OrganisationFactory()
        client = APIClient()
        response = client.get(
            '%s/organisations/%s' % (self.base_url, Organisation.objects.get(name="The nappy changers").id),
            format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(r['name'], "The nappy changers")
        self.assertEqual(response.status_code, 200)

    def test_get_organisation_many(self):
        OrganisationFactory()  # TODO: refactor to create n orgs
        OrganisationFactory(name="Another Organisation")
        client = APIClient()
        response = client.get('%s/organisations' % self.base_url, format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(r['count'], 2)
        self.assertEqual(response.status_code, 200)

    def test_get_organisation_four_oh_fours(self):
        client = APIClient()
        response = client.get('%s/sites/%s' % (self.base_url, 999), format='json', secure=True)
        self.assertEqual(response.status_code, 404)

    def test_get_organisation_none(self):
        client = APIClient()
        response = client.get('%s/organisations' % self.base_url, format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(r['count'], 0)
        self.assertEqual(response.status_code, 200)

    """ Update """

    def test_update_organisation(self):
        OrganisationFactory()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = self.organisation_json
        data["name"] = "The body snatchers"
        response = client.put(
            '%s/organisations/%s' % (self.base_url, Organisation.objects.get(name="The nappy changers").id), data=data,
            format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(r['name'], "The body snatchers")
        self.assertEqual(response.status_code, 200)

    def test_update_organisation_four_oh_fours(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.put('%s/organisations/%s' % (self.base_url, 999), self.organisation_json, format='json',
                              secure=True)
        self.assertEqual(response.status_code, 404)

    def test_update_organisation_requires_authentication(self):
        OrganisationFactory()
        client = APIClient()
        response = client.put(
            '%s/organisations/%s' % (self.base_url, Organisation.objects.get(name="The nappy changers").id),
            self.organisation_json, format='json', secure=True)
        self.assertEqual(response.status_code, 401)

    """ Delete """

    def test_delete_organisation(self):
        OrganisationFactory()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.delete(
            '%s/organisations/%s' % (self.base_url, Organisation.objects.get(name="The nappy changers").id),
            format='json', secure=True)
        self.assertEqual(Site.objects.count(), 0)
        self.assertEqual(response.status_code, 204)

    def test_delete_organisation_requires_authentications(self):
        OrganisationFactory()
        client = APIClient()
        response = client.delete(
            '%s/organisations/%s' % (self.base_url, Organisation.objects.get(name="The nappy changers").id),
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
        self.assertEqual(r['name'], "Do Gooders")
        self.assertEqual(r['url'], "www.example.com/dogooders/jobs")
        self.assertEqual(response.status_code, 201)

    def test_create_site_requires_authentications(self):
        client = APIClient()
        response = client.post('%s/sites' % self.base_url,
                               {'name': 'Do Gooders', 'url': 'www.example.com/dogooders/jobs'}, format='json',
                               secure=True)
        self.assertEqual(response.status_code, 401)

    """ Read """

    def test_get_sites_one(self):
        SiteFactory()
        client = APIClient()
        response = client.get('%s/sites/%s' % (self.base_url, Site.objects.get(name="Greenpeace").id), format='json',
                              secure=True)
        r = json.loads(response.content)
        self.assertEqual(r['name'], "Greenpeace")
        self.assertEqual(response.status_code, 200)

    def test_get_sites_many(self):
        SiteFactory()
        SiteFactory(name="Another Site")
        client = APIClient()
        response = client.get('%s/sites' % self.base_url, format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(r['count'], 2)
        self.assertEqual(response.status_code, 200)

    def test_get_site_four_oh_fours(self):
        client = APIClient()
        response = client.get('%s/sites/%s' % (self.base_url, 999), format='json', secure=True)
        self.assertEqual(response.status_code, 404)

    def test_get_sites_none(self):
        client = APIClient()
        response = client.get('%s/sites' % self.base_url, format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(r['count'], 0)
        self.assertEqual(response.status_code, 200)

    """ Update """

    def test_update_sites(self):
        SiteFactory()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {'name': 'Clowns for Justice', 'url': 'www.example.com/dogooders/jobs'}
        response = client.put('%s/sites/%s' % (self.base_url, Site.objects.get(name="Greenpeace").id), data=data,
                              format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(r['name'], "Clowns for Justice")
        self.assertEqual(response.status_code, 200)

    def test_update_sites_four_oh_fours(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.put('%s/sites/%s' % (self.base_url, 999),
                              {'name': 'Do Gooders', 'url': 'www.example.com/dogooders/jobs'}, format='json',
                              secure=True)
        self.assertEqual(response.status_code, 404)

    def test_update_sites_requires_authentications(self):
        SiteFactory()
        client = APIClient()
        response = client.put('%s/sites/%s' % (self.base_url, Site.objects.get(name="Greenpeace").id),
                              {'name': 'Do Gooders', 'url': 'www.example.com/dogooders/jobs'}, format='json',
                              secure=True)
        self.assertEqual(response.status_code, 401)

    """ Delete """

    def test_delete_site(self):
        SiteFactory()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.delete('%s/sites/%s' % (self.base_url, Site.objects.get(name="Greenpeace").id), format='json',
                                 secure=True)
        self.assertEqual(Site.objects.count(), 0)
        self.assertEqual(response.status_code, 204)

    def test_delete_site_requires_authentications(self):
        SiteFactory()
        client = APIClient()
        response = client.delete('%s/sites/%s' % (self.base_url, Site.objects.get(name="Greenpeace").id), format='json',
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
        LabelsFactory()
        OrganisationFactory()
        SiteFactory()

        data = self.job_json
        data['labels'] = [Labels.objects.get(name="people").id]
        data['sites'] = [Site.objects.get(name="Greenpeace").id]
        data['organisation_id'] = Organisation.objects.get(name="The nappy changers").id

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        response = client.post('%s/jobs' % self.base_url, data=data, format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(r['title'], "Eternal Gardener")
        self.assertEqual(r['text'], "for the nature lover")
        self.assertEqual(r['sites'], data['sites'])
        self.assertEqual(r['labels'], data['labels'])
        self.assertEqual(response.status_code, 201)

    def test_create_job_no_auth(self):
        client = APIClient()
        response = client.post('%s/labels' % self.base_url, self.job_json, format='json', secure=True)
        self.assertEqual(response.status_code, 401)

        """ Read """

    def test_get_jobs_one(self):
        JobFactory.create()
        client = APIClient()
        response = client.get('%s/jobs/%s' % (self.base_url, Job.objects.get(title="Nappy changer").id), format='json',
                              secure=True)
        r = json.loads(response.content)
        self.assertEqual(r['title'], "Nappy changer")
        self.assertEqual(response.status_code, 200)

    def test_get_jobs_many(self):
        JobFactory.create()  # TODO could automatically create n
        JobFactory.create(title="Trail builder")
        client = APIClient()
        response = client.get('%s/jobs' % (self.base_url), format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(r['count'], 2)
        self.assertEqual(response.status_code, 200)

    def test_get_jobs_none(self):
        client = APIClient()
        response = client.get('%s/jobs' % (self.base_url), format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(r['count'], 0)
        self.assertEqual(response.status_code, 200)

    def test_get_jobs_four_oh_fours(self):
        client = APIClient()
        response = client.get('%s/jobs/%s' % (self.base_url, 999), format='json', secure=True)
        self.assertEqual(response.status_code, 404)

    """ Update """

    def test_update_jobs(self):
        SiteFactory()
        LabelsFactory()
        JobFactory.create()

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = self.job_json  # TODO: currently fails because json referes to org id that is not there
        data["title"] = "Clown"
        data["organisation_id"] = Organisation.objects.get().id
        data["sites"] = [Site.objects.get(name="Greenpeace").id]
        data["labels"] = [Labels.objects.get(name="people").id]
        response = client.put('%s/jobs/%s' % (self.base_url, Job.objects.get(title="Nappy changer").id), data=data,
                              format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(r['title'], "Clown")
        self.assertEqual(response.status_code, 200)

    def test_update_jobs_four_oh_fours(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.put('%s/jobs/%s' % (self.base_url, 999), self.job_json, format='json', secure=True)
        self.assertEqual(response.status_code, 404)

    def test_update_jobs_requires_authentications(self):
        JobFactory.create()
        client = APIClient()
        data = self.job_json
        response = client.put('%s/jobs/%s' % (self.base_url, Job.objects.get(title="Nappy changer").id), data=data,
                              format='json', secure=True)
        self.assertEqual(response.status_code, 401)

    """ Delete """

    def test_delete_jobs(self):
        JobFactory.create()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        length = Job.objects.count()
        response = client.delete('%s/jobs/%s' % (self.base_url, Job.objects.get(title="Nappy changer").id),
                                 format='json', secure=True)
        length -= 1
        self.assertEqual(Job.objects.count(), length)
        self.assertEqual(response.status_code, 204)

    def test_delete_jobs_requires_authentications(self):
        JobFactory.create()
        client = APIClient()
        response = client.delete('%s/jobs/%s' % (self.base_url, Job.objects.get(title="Nappy changer").id),
                                 format='json', secure=True)
        self.assertEqual(response.status_code, 401)

    def test_delete_jobs_four_oh_fours(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.delete('%s/jobs/%s' % (self.base_url, 999), format='json', secure=True)
        self.assertEqual(response.status_code, 404)
