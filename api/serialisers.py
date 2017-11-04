from rest_framework import serializers

from vol.models import Labels, Organisation, Site, Job


class LabelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Labels
        fields = ['uuid', 'name', 'created_at', 'updated_at']
        lookup_field = 'uuid'


class OrganisationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organisation
        fields = ('uuid', 'name', 'description', 'country', 'region', 'city', 'url', 'created_at', 'updated_at')
        lookup_field = 'uuid'


class SiteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Site
        fields = ('uuid', 'name', 'url', 'created_at', 'updated_at')
        lookup_field = 'uuid'


class JobSerializer(serializers.HyperlinkedModelSerializer):
    organisation = OrganisationSerializer(read_only=True)
    labels = serializers.PrimaryKeyRelatedField(queryset=Labels.objects.all(), many=True)
    sites = serializers.PrimaryKeyRelatedField(queryset=Site.objects.all(), many=True)

    # organisation = OrganisationSerializer()
    # labels = LabelSerializer(many=True)
    # sites = SiteSerializer(many=True)

    # Dang, need to fix this to work by uuid now..
    organisation_uuid = serializers.PrimaryKeyRelatedField(
        queryset=Organisation.objects.all(), source='organisation', write_only=True)

    class Meta:
        model = Job
        fields = ('uuid', 'title', 'text', 'labels', 'organisation', 'organisation_uuid',
                  'sites', 'country', 'city', 'region', 'created_at', 'updated_at', 'url', 'seen')
        lookup_field = 'uuid'
