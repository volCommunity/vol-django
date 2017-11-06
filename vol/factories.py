import factory

from .models import Job, Labels, Site, Organisation


class LabelsFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'label {0}'.format(n))

    class Meta:
        model = Labels
        django_get_or_create = ('name',)


class SiteFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Site {0}'.format(n))
    url = factory.Sequence(lambda n: 'http://www.{0}.site'.format(n))

    class Meta:
        model = Site
        django_get_or_create = ('name', 'url')


class OrganisationFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Organisation {0}'.format(n))
    country = "NZ"
    city = "wellington"
    region = "wellington"
    description = "some org"
    url = factory.Sequence(lambda n: 'http://www.{0}.org'.format(n))

    class Meta:
        model = Organisation
        django_get_or_create = ('name', 'url')


class JobFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: 'Job title {0}'.format(n))
    text = "A create opportunity for a people person"
    country = "NZ"
    region = "wellington"
    city = "wellington"
    url = factory.Sequence(lambda n: 'http://www.example.org/job/{0}'.format(n))
    seen = 0

    organisation = factory.SubFactory(OrganisationFactory)

    class Meta:
        model = Job
        django_get_or_create = ('title', 'url')
