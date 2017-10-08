from datetime import datetime

from django.test import TestCase

from .models import Job, Labels, Site, Organisation


class JobTestCase(TestCase):
    def setUp(self):
        Organisation.objects.create(name="The nappy changers",
                                    country="New Zealand",
                                    city="Wellington",
                                    region="Wellington",
                                    url="www.example.com/organisations/nappychangers",
                                    )
        Organisation.objects.create(name="The Elysium fields",
                                    country="New Zealand",
                                    city="Wellington",
                                    region="Wellington",
                                    url="www.example.com/organisations/elysiumfields",
                                    )
        Labels.objects.create(name="people")
        Labels.objects.create(name="nature")

        Site.objects.create(name="Do Gooders",
                            url="www.exapmple.com/dogooders/jobs")

        Site.objects.create(name="Green as Grass",
                            url="www.exapmple.com/gag/jobs")

        self.job1 = Job.objects.create(title="Nappy changer",
                           text="A create opportunity for a people person",
                           organisation=Organisation.objects.get(name="The nappy changers"),
                           country="NZ",
                           region="Wellington",
                           city="Wellington",
                           url="http://www.example.com/jobs/1",
                           seen=0
                           )

        # Add one label for *_one tests
        self.job1.labels.add(Labels.objects.get(name="nature"))
        self.job1.sites.add(Site.objects.get(name="Do Gooders"))

        self.job2 = Job.objects.create(title="Eternal Gardener",
                           text="for the nature lover",
                           organisation=Organisation.objects.get(name="The Elysium fields"),
                           country="NZ",
                           region="Wellington",
                           city="Wellington",
                           url="http://www.example.com/jobs/2",
                           seen=0
                           )

        # Add 2 labels for *_many tests
        self.job2.labels.add(Labels.objects.get(name="people"))
        self.job2.labels.add(Labels.objects.get(name="nature"))
        self.job2.sites.add(Site.objects.get(name="Green as Grass"))

    # TODO: think of scenarios where we can actually test some added
    # logic, this just tests standard Django things. If there is nothing
    # to test, are we doing enough in regards to validation or normalisation
    # think of things like undercasing, replacing spaces with -, things that
    # we now do in view but might belong in the models themselves.
    # See http://www.tangowithdjango.com/book17/chapters/test.html
    def test_find_job_none(self):
        self.assertFalse(Job.objects.filter(labels__name="exorcism").exists())

    def test_find_job_one(self):
        self.assertEqual(len(Job.objects.filter(labels__name="people")), 1)

    def test_find_job_many(self):
        self.assertEqual(len(Job.objects.filter(labels__name="nature")), 2)

    def test_find_organisation_none(self):
        self.assertFalse(Organisation.objects.filter(name="The Exorcists").exists())

    def test_find_organisation_one(self):
        self.assertEqual(len(Organisation.objects.filter(name="The nappy changers")), 1)

    def test_find_organisation_many(self):
        self.assertEqual(len(Organisation.objects.filter(city="Wellington")), 2)

    def test_find_labels_none(self):
        self.assertFalse(Labels.objects.filter(name="exorcism").exists())

    def test_find_labels_one(self):
        self.assertEqual(len(Labels.objects.filter(name="people")), 1)