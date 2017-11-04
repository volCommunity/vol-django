from rest_framework import viewsets

from vol.models import Labels, Organisation, Site, Job
from .serialisers import JobSerializer, OrganisationSerializer, SiteSerializer, LabelSerializer


class LabelViewSet(viewsets.ModelViewSet):
    """
    list:
    API endpoint that returns a list of labels.

    create:
    API endpoint that creates a new label resource.

    partial_update:
    Not implemented.

    update:
    API endpoint that  updates an existing label resource.

    delete:
    API endpoint that deletes a label resource.
    """
    filter_fields = ('uuid', 'name', 'created_at', 'updated_at')

    queryset = Labels.objects.all()
    serializer_class = LabelSerializer
    lookup_field = 'uuid'


class OrganisationViewSet(viewsets.ModelViewSet):
    """
    list:
    API endpoint that returns a list of organisations.

    create:
    API endpoint that creates a new organisation resource.

    partial_update:
    Not implemented.

    update:
    API endpoint that  updates an existing organisation resource.

    delete:
    API endpoint that deletes a organisation resource.
    """
    filter_fields = ('uuid', 'name', 'description', 'country', 'region', 'city', 'url', 'created_at', 'updated_at')

    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    lookup_field = 'uuid'


class SiteViewSet(viewsets.ModelViewSet):
    """
    list:
    API endpoint that returns a list of sites.

    create:
    API endpoint that creates a new site resource.

    partial_update:
    Not implemented.

    update:
    API endpoint that  updates an existing site resource.

    delete:
    API endpoint that deletes a site resource.
    """
    filter_fields = ('uuid', 'name', 'url', 'created_at', 'updated_at')

    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    lookup_field = 'uuid'


class JobViewSet(viewsets.ModelViewSet):
    """
    list:
    API endpoint that returns a list of jobs.

    create:
    API endpoint that creates a new job resource.

    partial_update:
    Not implemented.

    update:
    API endpoint that  updates an existing job resource.

    Note that the existing job will be updated, for nested resources the behaviour is as follows:\n
    Organisation - If the organisation exists it will be linked, if it does not it will
        be created. If the organisation included is invalid a validation error will be raised.\n
    Labels - If an empty list is passed, current labels are removed from the
        instance. If the list contains labels, a label will be created or if it exists
        that resource will be linked. \n
    Sites - If an empty list is passed, current labels are removed from the
        instance. If the list contains labels, a label will be created or if it exists
        that resource will be linked. If any of the sites is invalid a validation will be raised.

    delete:
    API endpoint that deletes a job resource.
    """
    filter_fields = ('uuid', 'title', 'text', 'labels', 'organisation', 'sites',
                     'country', 'region', 'city', 'created_at', 'updated_at',
                     'url', 'seen')

    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = 'uuid'
