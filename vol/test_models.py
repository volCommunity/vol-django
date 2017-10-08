from django.test import TestCase
from datetime import datetime

from .models import Job, Labels, Site, Organisation

class JobTestCase(TestCase):
    def setUp(self):
        Organisation.objects.create(name="The nappy changers",
                                    country="New Zealand",
                                    city="Wellington",
                                    region="Wellington",
                                    url="www.example.com/organisations/nappychangers",
                                    added=datetime.now())

        Organisation.objects.create(name="The Elysium fields",
                                    country="New Zealand",
                                    city="Wellington",
                                    region="Wellington",
                                    url="www.example.com/organisations/elysiumfields",
                                    added=datetime.now())

        Labels.object.create(name="people",
                                     added=datetime.now())

        Labels.object.create(name="nature",
                             added=datetime.now())

        Site.objects.create(name="Do Gooders",
                                   url = "www.exapmple.com/dogooders/jobs",
                                   added=datetime.now())

        Site.objects.create(name="Green as Grass",
                            url = "www.exapmple.com/gag/jobs",
                            added=datetime.now())

        Job.objects.create(title="Nappy changer",
                           text="A create opportunity for a people person",
                           labels=Labels.objects.get(name="people"),
                           organisation=Organisation.objects.get(name="The nappy changers""),
                           site=Site.objectss.get(name="Do Gooders",
                           country="NZ",
                           region="Wellington",
                           city="Wellington",
                           added=datetime.now(),
                           url="http://www.example.com/jobs/1",
                           seen=0
                           )

        Job.objects.create(title="Eternal Gardener",
                                 text="for the nature lover",
                                 labels=Labels.objects.get(name="nature"),
                                 organisation=Organisation.objects.get(name="The Elysium fields"),
                                 site=Site.objects.get(name="Green as Grass"),
                                 country="NZ",
                                 region="Wellington",
                                 city="Wellington",
                                 added=datetime.now(),
                                 url="http://www.example.com/jobs/2",
                                 seen=0
                                 )

    # TODO: define some sensible test scenarios
    def find_job_none(self):
        jobs = Job.objects.filter(labels__name="exocism")
        self.assertIsNone(jobs)
