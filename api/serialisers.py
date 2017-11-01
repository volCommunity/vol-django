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
    """ JobSerialiser serializes Job objects. It includes a few nested serialisers to allow
        writing of nested objects.

        These nested serialisers have validators disabled. Removing the validator allows us
        to do create and update operations on Jobs, while including Labels, Organisations and
         Sites that may or may not exist.
    """

    class NestedLabelSerializer(LabelSerializer):
        class Meta(LabelSerializer.Meta):
            extra_kwargs = {
                'name': {
                    'validators': []
                }
            }

    class NestedOrganisationSerializer(OrganisationSerializer):
        class Meta(OrganisationSerializer.Meta):
            extra_kwargs = {
                'name': {
                    'validators': []
                }
            }

    class NestedSiteSerializer(SiteSerializer):
        class Meta(SiteSerializer.Meta):
            extra_kwargs = {
                'url': {
                    'validators': []
                }
            }

    organisation = NestedOrganisationSerializer()
    labels = NestedLabelSerializer(many=True)
    sites = NestedSiteSerializer(many=True)

    class Meta:
        model = Job
        fields = ('uuid', 'title', 'text', 'labels', 'organisation',
                  'sites', 'country', 'city', 'region', 'created_at', 'updated_at', 'url', 'seen')
        lookup_field = 'uuid'

    def create(self, validated_data):
        """
        Override create() and handle nested objects manually.

        :param validated_data:
        :return Job:
        """
        organisation = validated_data.pop('organisation')
        labels = validated_data.pop('labels')
        sites = validated_data.pop('sites')

        org, created = Organisation.objects.get_or_create(**organisation)

        created_labels = []
        for label in labels:
            l, created = Labels.objects.get_or_create(name=label['name'])
            created_labels.append(l)

        created_sites = []
        for site in sites:
            s, created = Site.objects.get_or_create(name=site['name'],
                                                    url=site['url'])
        created_sites.append(s)

        # Create the Job object and provide it with the organisation ID we got or created before
        j = Job.objects.create(organisation_id=org.id, **validated_data)

        # Job done, now that we have the IDs of both side of the many 2 many relationship we can finally establish it.
        j.labels = created_labels
        j.sites = created_sites

        return j

    def update(self, instance, validated_data):
        """
        Override update() and handle nested objects manually.

        :param instance:
        :param validated_data:
        :return Job:
        """
        pass
