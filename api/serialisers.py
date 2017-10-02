from vol.models import Labels, Organisation, Site, Job

from rest_framework import serializers

# TODO: Add all models, fix "interesting" relationships
class JobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Job
        fields = ('title', 'text')