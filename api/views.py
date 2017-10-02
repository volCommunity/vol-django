from django.contrib.auth.models import User, Group
from vol.models import Labels, Organisation, Site, Job
from rest_framework import viewsets
from .serialisers import JobSerializer

class JobViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Jobs to be viewed or edited.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer

