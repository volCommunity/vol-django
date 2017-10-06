from vol.models import Labels, Organisation, Site, Job
from rest_framework import viewsets
from .serialisers import JobSerializer, OrganisationSerializer, SiteSerializer, LabelSerializer


class LabelViewSet(viewsets.ModelViewSet):
    """
            API endpoint that allows Labels to be viewed or edited.
    """
    queryset = Labels.objects.all()
    serializer_class = LabelSerializer


class OrganisationViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows Organisations to be viewed or edited.

    """
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer


class SiteViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows Sites to be viewed or edited.
    """
    queryset = Site.objects.all()
    serializer_class = SiteSerializer


class JobViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Jobs to be viewed or edited.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer
