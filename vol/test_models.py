from django.test import TestCase

from vol.factories import LabelsFactory, OrganisationFactory, SiteFactory, JobFactory
from .models import Job, Labels, Site, Organisation


class JobTestCase(TestCase):

    def test_label_creation(self):
        label = LabelsFactory()
        self.assertTrue(isinstance(label, Labels))
        self.assertEqual(label.__str__(), label.name)

    def test_organisation_creation(self):
        organisation = OrganisationFactory()
        self.assertTrue(isinstance(organisation, Organisation))
        self.assertEqual(organisation.__str__(), organisation.name)

    def test_site_creation(self):
        site = SiteFactory()
        self.assertTrue(isinstance(site, Site))
        self.assertEqual(site.__str__(), site.name)

    def test_job_creation(self):
        job = JobFactory()
        self.assertTrue(isinstance(job, Job))
        self.assertEqual(job.__str__(), job.title)
