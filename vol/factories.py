import factory

from .models import Job, Labels, Site, Organisation


class LabelsFactory(factory.django.DjangoModelFactory):
    name = "people"

    class Meta:
        model = Labels


class SiteFactory(factory.django.DjangoModelFactory):
    name = "Greenpeace"
    url = "www.example.com/gp/jobs"

    class Meta:
        model = Site


class OrganisationFactory(factory.django.DjangoModelFactory):
    name = "The nappy changers"
    country = "NZ"
    city = "Wellington"
    region = "Wellington"
    url = "www.example.com/organisations/nappychangers"

    class Meta:
        model = Organisation


class JobFactory(factory.django.DjangoModelFactory):
    title = "Nappy changer"
    text = "A create opportunity for a people person"
    country = "NZ"
    region = "Welington"
    city = "Wellington"
    url = "http://www.example.com/jobs/1"
    seen = 0

    organisation = factory.SubFactory(OrganisationFactory)

    class Meta:
        model = Job