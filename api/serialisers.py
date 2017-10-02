from vol.models import Labels, Organisation, Site, Job

from rest_framework import serializers

class LabelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Labels
        fields = ['name']

class OrganisationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organisation
        fields = ('name', 'region', 'city', 'url', 'added')

class SiteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Site
        fields = ('name', 'url', 'added')

class JobSerializer(serializers.HyperlinkedModelSerializer):
    labels = LabelSerializer(read_only=True, many=True)
    site = SiteSerializer(read_only=True, many=True)
    organisation = serializers.RelatedField(read_only=True)
    organisation = OrganisationSerializer(read_only=True)

    class Meta:
        model = Job
        fields = ('title', 'text', 'labels', 'organisation',
                  'site', 'country', 'region', 'added', 'url', 'seen')