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
        organisation_data = validated_data.pop('organisation')
        labels_data = validated_data.pop('labels')
        sites_data = validated_data.pop('sites')

        o = Organisation.objects.get(name=organisation_data['name'])
        # TODO: handle the other fields too, add short doco
        if o and o.country != organisation_data['country']:
            # TODO: be more helpful
            raise serializers.ValidationError("I'm afraid I can't do that, Dave")
        organisation, _ = Organisation.objects.get_or_create(**organisation_data)

        labels = []
        for label_data_item in labels_data:
            label, _ = Labels.objects.get_or_create(name=label_data_item['name'])
            labels.append(label)

        sites = []
        for site_data_item in sites_data:
            """ Search on the unique key: url, if we get it,
                check if the name matches, if it does not, we have to
                inform our users that this can never work out (or we
                will receive a nice foreign key constraint from our
                database
            """
            s = Site.objects.get(url=site_data_item['url'])
            if s and s.name != site_data_item['name']:
                # TODO: be more helpful
                raise serializers.ValidationError("I'm afraid I can't do that, Dave")
            site, _ = Site.objects.get_or_create(name=site_data_item['name'],
                                                 url=site_data_item['url'])
            sites.append(site)

        # Create the Job object and provide it with the organisation ID we got or created before
        j = Job.objects.create(organisation_id=organisation.id, **validated_data)

        # Job done, now that we have the IDs of both side of the many 2 many relationship we can finally establish it.
        j.labels = labels
        j.sites = sites

        return j

    def update(self, instance, validated_data):
        """
        Override update() and handle nested objects manually.

        :param instance:
        :param validated_data:
        :return Job:
        """

        organisation_data = validated_data.pop('organisation')
        labels_data = validated_data.pop('labels')
        sites_data = validated_data.pop('sites')

        # Update existing Job object
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.country = validated_data.get('country', instance.country)
        instance.region = validated_data.get('country', instance.region)
        instance.city = validated_data.get('city', instance.city)
        instance.url = validated_data.get('url', instance.url)
        instance.seen = validated_data.get('seen', instance.seen)

        # TODO: how to we interpret updates? deletion; no
        # updating; could raise, but would that be expected?

        labels = []
        # Get to work on the labels
        for label in labels_data:
            l, _ = Labels.objects.update_or_create(name=label['name'])
            labels.append(l)
        # Next sites
        sites = []
        for site in sites_data:
            # TODO: add validator and corresponding validator test
            s, _ = Site.objects.update_or_create(name=site['name'],
                                                 url=site['url'])
            sites.append(s)

        instance.labels = labels
        instance.sites = sites

        # TODO: add validator and corresponding validator test
        instance.organisation, _ = Organisation.objects.update_or_create(
            name=organisation_data.get('name', instance.organisation.name),
            description=organisation_data.get('description', instance.organisation.description),
            country=organisation_data.get('country', instance.organisation.country),
            region=organisation_data.get('region', instance.organisation.region),
            city=organisation_data.get('city', instance.organisation.city),
            url=organisation_data.get('url', instance.organisation.url),
        )

        instance.organisation.save()
        instance.save()

        return instance
