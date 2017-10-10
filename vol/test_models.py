from django.test import TestCase

from vol.factories import LabelsFactory, OrganisationFactory, SiteFactory, JobFactory
from .models import Job, Labels, Site, Organisation


class JobTestCase(TestCase):

    def test_label_creation(self):
        l = LabelsFactory()
        self.assertTrue(isinstance(l, Labels))
        self.assertEqual(l.__str__(), l.name)

    def test_organisation_creation(self):
        o = OrganisationFactory()
        self.assertTrue(isinstance(o, Organisation))
        self.assertEqual(o.__str__(), o.name)

    def test_site_creation(self):
        s = SiteFactory()
        self.assertTrue(isinstance(s, Site))
        self.assertEqual(s.__str__(), s.name)

    def test_job_creation(self):
        j = JobFactory()
        self.assertTrue(isinstance(j, Job))
        self.assertEqual(j.__str__(), j.title)
