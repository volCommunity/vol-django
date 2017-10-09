import json

from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from vol.models import Labels, Organisation, Site, Job

""" Create tests for:
 get, create (verify only auth), update (verify only auth), delete (verify only auth)
"""


class IndexViewTests(APITestCase):
    # TODO: find version using API, or do support YOLO clients.
    def setUp(self):
        self.base_url = "/api/%s" % "v0.0.1"
        # TODO: don't be lazy and create roles too, and use a less privileged user
        user = User.objects.create_superuser('admin', 'admin@example.com', 'test123')
        self.token = Token.objects.create(user=user)

        # TODO: use factory boy
        # Things that we'l create in our tests
        self.job_json = {"title": "Eternal Gardener",
                         "text": "for the nature lover",
                         "organisation_id": 1, # TODO: get this dynamically
                         "country": "NZ",
                         "region": "Wellington",
                         "city": "Wellington",
                         "url":"http://www.example.com/jobs/2",
                         "seen": 0,
                         "labels": [1], # TODO: get this dynamically
                         "sites": [1]}  # TODO: get this dynamically
        self.site_json = {'name': 'Do Gooders', 'url': 'www.example.com/dogooders/jobs'}
        self.label_json = {'name': 'nature'}
        self.organisation_json = {'name': 'nature'}

        # Things we'll set up in the db, TODO: consider moving to be in fixtures
        Organisation.objects.create(name="The nappy changers",
                                    country="New Zealand",
                                    city="Wellington",
                                    region="Wellington",
                                    url="www.example.com/organisations/nappychangers",
                                    )
        Labels.objects.create(name="people")
        Labels.objects.create(name="outdoors")
        Site.objects.create(name="Green as Grass",
                            url="www.example.com/gag/jobs")
        Site.objects.create(name="Greenpeace",
                            url="www.example.com/gp/jobs")

        # TODO: use factory boy
        j = Job.objects.create(title="Nappy changer",
                                       text="A create opportunity for a people person",
                                       organisation=Organisation.objects.get(name="The nappy changers"),
                                       country="NZ",
                                       region="Wellington",
                                       city="Wellington",
                                       url="http://www.example.com/jobs/1",
                                       seen=0
                                       )

        # Add one label for *_one tests
        j.labels.add(Labels.objects.get(name="people"))
        j.sites.add(Site.objects.get(name="Green as Grass"))

    # Assert we are redirected to a secure url
    def test_index_insecure_redirects(self):
        response = self.client.get('/api', secure=False)
        self.assertEqual(response.status_code, 301)

    def test_index_view(self):
        response = self.client.get('/api', secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "labels")

    """ Labels CRUD
        Create """
    def test_create_label_auth(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        length = Labels.objects.count()
        response = client.post('%s/labels' % self.base_url, self.label_json, format='json', secure=True)
        length += 1
        self.assertEqual(Labels.objects.count(), length)
        self.assertEqual(Labels.objects.get(name="nature").name, 'nature')
        r = json.loads(response.content)
        self.assertEqual(r['name'], "nature")
        self.assertEqual(response.status_code, 201)

    def test_create_label_requires_authentications(self):
        client = APIClient()
        response = client.post('%s/labels' % self.base_url, self.label_json, format='json', secure=True)
        self.assertEqual(response.status_code, 401)

    """ Read """
    def test_get_labels_one(self):
        client = APIClient()
        response = client.get('%s/labels/%s' % (self.base_url, Labels.objects.get(name="people").id), format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(r['name'], "people")
        self.assertEqual(response.status_code, 200)

    def test_get_labels_many(self):
        client = APIClient()
        response = client.get('%s/labels' % (self.base_url), format='json', secure=True)
        r = json.loads(response.content)
        print("r: %s" % r)
        self.assertEqual(r['count'], 2)
        self.assertEqual(response.status_code, 200)

    def test_get_labels_none(self):
        client = APIClient()
        response = client.get('%s/labels/%s' % (self.base_url, 999), format='json', secure=True)
        self.assertEqual(response.status_code, 404)

    """ Update """
    def test_update_labels(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = self.label_json
        data["name"] = "clowns"
        response = client.put('%s/labels/%s' % (self.base_url, Labels.objects.get(name="people").id), self.label_json, format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(r['name'], "clowns")
        self.assertEqual(response.status_code, 200)

    def test_update_labels_four_oh_fours(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.put('%s/labels/%s' % (self.base_url, 999), self.label_json, format='json', secure=True)
        self.assertEqual(response.status_code, 404)

    def test_update_labels_requires_authentications(self):
        client = APIClient()
        data = self.label_json
        response = client.put('%s/labels/%s' % (self.base_url, Labels.objects.get(name="people").id), data=data, format='json', secure=True)
        self.assertEqual(response.status_code, 401)

    """ Delete """
    def test_delete_labels(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        length = Labels.objects.count()
        response = client.delete('%s/labels/%s' % (self.base_url, Labels.objects.get(name="people").id), format='json', secure=True)
        length -= 1
        self.assertEqual(Labels.objects.count(), length)
        self.assertEqual(response.status_code, 204)

    def test_delete_labels_requires_authentications(self):
        client = APIClient()
        response = client.delete('%s/labels/%s' % (self.base_url, Labels.objects.get(name="people").id), format='json', secure=True)
        self.assertEqual(response.status_code, 401)

    def test_delete_labels_four_oh_fours(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.delete('%s/labels/%s' % (self.base_url, 999), format='json', secure=True)
        self.assertEqual(response.status_code, 404)

    """ Sites CRUD
        Create """
    def test_create_site(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        length = Site.objects.count()
        response = client.post('%s/sites' % self.base_url, self.site_json, format='json', secure=True)
        length += 1
        self.assertEqual(Site.objects.count(), length)
        self.assertEqual(Site.objects.get(name="Do Gooders").name, 'Do Gooders')
        r = json.loads(response.content)
        self.assertEqual(r['name'], "Do Gooders")
        self.assertEqual(r['url'], "www.example.com/dogooders/jobs")
        self.assertEqual(response.status_code, 201)

    def test_create_site_requires_authentications(self):
        client = APIClient()
        response = client.post('%s/sites' % self.base_url, self.site_json, format='json', secure=True)
        self.assertEqual(response.status_code, 401)

    """ Read """
    def test_get_sites_one(self):
        client = APIClient()
        response = client.get('%s/sites/%s' % (self.base_url, Site.objects.get(name="Green as Grass").id), format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(r['name'], "Green as Grass")
        self.assertEqual(response.status_code, 200)

    def test_get_sites_many(self):
        client = APIClient()
        response = client.get('%s/sites' % (self.base_url), format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(r['count'], 2)
        self.assertEqual(response.status_code, 200)

    def test_get_sites_none(self):
        client = APIClient()
        response = client.get('%s/sites/%s' % (self.base_url, 999), format='json', secure=True)
        self.assertEqual(response.status_code, 404)

    """ Update """
    def test_update_sites(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = self.site_json
        data["name"] = "Clowns for Justice"
        response = client.put('%s/sites/%s' % (self.base_url, Site.objects.get(name="Green as Grass").id), data=data, format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(r['name'], "Clowns for Justice")
        self.assertEqual(response.status_code, 200)

    def test_update_sites_four_oh_fours(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.put('%s/sites/%s' % (self.base_url, 999), self.site_json, format='json', secure=True)
        self.assertEqual(response.status_code, 404)

    def test_update_sites_requires_authentications(self):
        client = APIClient()
        response = client.put('%s/sites/%s' % (self.base_url, Site.objects.get(name="Green as Grass").id), self.site_json, format='json', secure=True)
        self.assertEqual(response.status_code, 401)

    """ Delete """
    def test_delete_site(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        length = Site.objects.count()
        response = client.delete('%s/sites/%s' % (self.base_url, Site.objects.get(name="Green as Grass").id), format='json', secure=True)
        length -= 1
        self.assertEqual(Site.objects.count(), length)
        self.assertEqual(response.status_code, 204)

    def test_delete_site_requires_authentications(self):
        client = APIClient()
        response = client.delete('%s/sites/%s' % (self.base_url, Site.objects.get(name="Green as Grass").id), format='json', secure=True)
        self.assertEqual(response.status_code, 401)

    def test_delete_site_four_oh_fours(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.delete('%s/sites/%s' % (self.base_url, 999), format='json', secure=True)
        self.assertEqual(response.status_code, 404)

    """ Jobs CRUD
        Create """
    def test_create_job_auth(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        response = client.post('%s/jobs' % self.base_url, self.job_json, format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(r['title'], "Eternal Gardener")
        self.assertEqual(r['text'], "for the nature lover")
        self.assertEqual(r['sites'], [1])
        self.assertEqual(r['labels'], [1])
        self.assertEqual(response.status_code, 201)

    def test_create_job_no_auth(self):
        client = APIClient()
        response = client.post('%s/labels' % self.base_url, self.job_json, format='json', secure=True)
        self.assertEqual(response.status_code, 401)

        """ Read """
    def test_get_jobs_one(self):
        client = APIClient()
        response = client.get('%s/jobs/%s' % (self.base_url, Job.objects.get(title="Nappy changer").id), format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(r['title'], "Nappy changer")
        self.assertEqual(response.status_code, 200)

    def test_get_jobs_many(self):
        client = APIClient()
        response = client.get('%s/jobs' % (self.base_url), format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(r['count'], 1)
        self.assertEqual(response.status_code, 200)

    def test_get_jobs_none(self):
        client = APIClient()
        response = client.get('%s/jobs/%s' % (self.base_url, 999), format='json', secure=True)
        self.assertEqual(response.status_code, 404)

    """ Update """
    def test_update_jobs(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = self.job_json # TODO: currently fails because json referes to org id that is not there
        data["title"] = "Clown"
        data["organisation_id"] = Organisation.objects.get().id
        data["sites"] = [Site.objects.get(name="Greenpeace").id]
        data["labels"] = [Labels.objects.get(name="people").id]
        response = client.put('%s/jobs/%s' % (self.base_url, Job.objects.get(title="Nappy changer").id), data=data, format='json', secure=True)
        r = json.loads(response.content)
        self.assertEqual(r['title'], "Clown")
        self.assertEqual(response.status_code, 200)

    def test_update_jobs_four_oh_fours(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.put('%s/jobs/%s' % (self.base_url, 999), self.label_json, format='json', secure=True)
        self.assertEqual(response.status_code, 404)

    def test_update_jobs_requires_authentications(self):
        client = APIClient()
        data = self.label_json
        response = client.put('%s/jobs/%s' % (self.base_url, Job.objects.get(title="Nappy changer").id), data=data, format='json', secure=True)
        self.assertEqual(response.status_code, 401)

    """ Delete """
    def test_delete_jobs(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        length = Job.objects.count()
        response = client.delete('%s/jobs/%s' % (self.base_url, Job.objects.get(title="Nappy changer").id), format='json', secure=True)
        length -= 1
        self.assertEqual(Job.objects.count(), length)
        self.assertEqual(response.status_code, 204)

    def test_delete_jobs_requires_authentications(self):
        client = APIClient()
        response = client.delete('%s/jobs/%s' % (self.base_url, Job.objects.get(title="Nappy changer").id), format='json', secure=True)
        self.assertEqual(response.status_code, 401)

    def test_delete_jobs_four_oh_fours(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.delete('%s/jobs/%s' % (self.base_url, 999), format='json', secure=True)
        self.assertEqual(response.status_code, 404)
