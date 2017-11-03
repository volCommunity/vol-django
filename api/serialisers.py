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

        organisation, _ = Organisation.objects.get_or_create(**organisation_data)

        labels = []
        for label_data_item in labels_data:
            label, _ = Labels.objects.get_or_create(name=label_data_item['name'])
            labels.append(label)

        sites = []
        for site_data_item in sites_data:
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
        # print("Org received data: %s" % organisation_data)
        # print("Org existing data: %s" % organisation)
        labels_data = validated_data.pop('labels')
        sites_data = validated_data.pop('sites')

        # Update the existing Job object
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.country = validated_data.get('country', instance.country)
        instance.region = validated_data.get('country', instance.region)
        instance.city = validated_data.get('city', instance.city)
        instance.url = validated_data.get('url', instance.url)
        instance.seen = validated_data.get('seen', instance.seen)

        # TODO: * consider when things are removed
        labels = []  # TODO: what if order is reversed?
        for label in labels_data:
            l, _ = Labels.objects.update_or_create(name=label['name'])
            labels.append(l)

        sites = []
        for site in sites_data:
            s, _ = Site.objects.update_or_create(name=site['name'],
                                                 url=site['url'])
            sites.append(s)

        instance.labels = labels
        instance.sites = sites

        instance.organisation, _ = Organisation.objects.update_or_create(
            name=organisation_data.get('name', instance.organisation.name),
            description=organisation_data.get('description', instance.organisation.description),
            country=organisation_data.get('country', instance.organisation.country),
            region=organisation_data.get('region', instance.organisation.region),
            city=organisation_data.get('city', instance.organisation.city),
            url=organisation_data.get('url', instance.organisation.url),
        )

        instance.organisation.save()

        # new_name = Organisation.objects.get(name=organisation_data.get('name'))
        # if new_name:
        #     print("Found an org object matching name of PUT data")
        #     # If it exists, if the id is different, if it is, we need to change to it, depending
        #     # on your philosophy..
        #     if organisation.uuid != new_name.uuid:
        #         print("Org object matching PUT data is different to the one we are linked to!\n"
        #               "updating our org id to this and considering our work done")
        #         # There is an object with this name, but it is different than the current
        #         # org we are linked to, should we update to that one, what happens to the other data?
        #         # instance.organisation.id = new_name.id # fuck this is not what we want at all.
        #         instance.organisation = new_name # Did this create a new copy?
        #         organisation.save()
        #         print("Org name after save: %s" % instance.organisation.name)
        # else:
        #     instance.organisation, created = Organisation.objects.update_or_create(
        #         name=organisation_data.get('name', instance.organisation.name),
        #         description=organisation_data.get('description', instance.organisation.description),
        #         country=organisation_data.get('country', instance.organisation.country),
        #         region=organisation_data.get('region', instance.organisation.region),
        #         city=organisation_data.get('city', instance.organisation.city),
        #         url=organisation_data.get('url', instance.organisation.url),
        #     )
        #
        #     if created:
        #         print("Created new org object")
        #     # Otherwise update all the things
        #     # organisation.name = organisation_data.get('name', organisation.name)
        #     # organisation.description = organisation_data.get('description', organisation.description)
        #     # organisation.country = organisation_data.get('country', organisation.country)
        #     # organisation.region = organisation_data.get('region', organisation.region)
        #     # organisation.city = organisation_data.get('city', organisation.city)
        #     # organisation.url = organisation_data.get('url', organisation.url)
        #
        #     instance.organisation.save()

        # instance.organisation = organisation # Connect it to our inst
        instance.save()

        # print("Organisation now %s" % instance.organisation)

        return instance
