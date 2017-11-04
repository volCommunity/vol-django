from rest_framework import viewsets

from vol.models import Labels, Organisation, Site, Job
from .serialisers import JobSerializer, OrganisationSerializer, SiteSerializer, LabelSerializer


class LabelViewSet(viewsets.ModelViewSet):
    """
            API endpoint that allows Labels to be viewed or edited.
    """
    filter_fields = ('uuid', 'name', 'created_at', 'updated_at')

    queryset = Labels.objects.all()
    serializer_class = LabelSerializer
    lookup_field = 'uuid'


class OrganisationViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows Organisations to be viewed or edited.

    """
    filter_fields = ('uuid', 'name', 'description', 'country', 'region', 'city', 'url', 'created_at', 'updated_at')

    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    lookup_field = 'uuid'


class SiteViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows Sites to be viewed or edited.
    """
    filter_fields = ('uuid', 'name', 'url', 'created_at', 'updated_at')

    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    lookup_field = 'uuid'


class JobViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Jobs to be viewed or edited.
    """
    filter_fields = ('uuid', 'title', 'text', 'labels', 'organisation', 'sites',
                     'country', 'region', 'city', 'created_at', 'updated_at',
                     'url', 'seen')

    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = 'uuid'
