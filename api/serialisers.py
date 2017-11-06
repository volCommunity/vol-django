from django.core.exceptions import ObjectDoesNotExist
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
    """ JobSerializer serializes Job objects. It includes a few nested serializers to allow
        writing of nested objects, and overridden create and update methods to allow writing.

        These nested serializers have validators disabled. Removing the validator allows us
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

    organisation = NestedOrganisationSerializer(required=False)
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
        labels = process_labels(validated_data.pop('labels'))
        sites = process_sites(validated_data.pop('sites'))

        if "organisation" in validated_data:
            organisation = self.process_organisation(validated_data.pop('organisation'), action='create')
            validated_data['organisation_id'] = organisation.id

        job = Job.objects.create(**validated_data)

        # Establish many 2 many relationships now that both side of the relationships
        # have been created and have an ID.
        job.labels = labels
        job.sites = sites

        return job

    def update(self, instance, validated_data):
        """
        Override update() and handle nested objects manually.

        :param instance:
        :param validated_data:
        :return Job:
        """

        # Update existing Job object
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.country = validated_data.get('country', instance.country)
        instance.region = validated_data.get('country', instance.region)
        instance.city = validated_data.get('city', instance.city)
        instance.url = validated_data.get('url', instance.url)
        instance.seen = validated_data.get('seen', instance.seen)

        if "labels" in validated_data:
            instance.labels = process_labels(validated_data.pop('labels'))
        if "sites" in validated_data:
            instance.sites = process_sites(validated_data.pop('sites'))
        if "organisation" in validated_data:
            instance.organisation = self.process_organisation(validated_data.pop('organisation'), action='update')

        instance.save()

        return instance

    def process_organisation(self, organisation_data, action=create):
        """
        Validates if an organisation with an identical name exists, if it does we assert it the same;
        updating the organisation is beyond our scope. Return organisation data if validation succeeeds.

        :param organisation_data:
        :param action:
        :raises ValidationError:
        """
        validate_organisation_if_there(organisation_data)

        if action == "create":
            organisation, _ = Organisation.objects.get_or_create(**organisation_data)
            return organisation

        if action == "update":
            self.instance.organisation, _ = Organisation.objects.get_or_create(
                name=organisation_data.get('name', self.instance.organisation.name),
                description=organisation_data.get('description', self.instance.organisation.description),
                country=organisation_data.get('country', self.instance.organisation.country),
                region=organisation_data.get('region', self.instance.organisation.region),
                city=organisation_data.get('city', self.instance.organisation.city),
                url=organisation_data.get('url', self.instance.organisation.url),
            )
            return self.instance.organisation


def validate_organisation_if_there(organisation_data):
    try:
        organisation_object = Organisation.objects.get(name=organisation_data['name'])
        field_list = ['description', 'country', 'region', 'city', 'url']  # TODO: can we generate this?
        if organisation_object:
            for field in field_list:
                if getattr(organisation_object, field) != organisation_data.get(field):
                    raise serializers.ValidationError(
                        "Organisation failed to pass validation: different organisation with identical name found")
    except ObjectDoesNotExist:
        pass


def process_sites(sites_data):
    """
    Generate a list of sites, if any, that are valid. Valid means that there is no
    pre-existing resource with an identical name, as that has a unique key constraint.

    We need to implement this as the automatically generated validator for the Site model was
    disabled in NestedOrganisationSerializer for nested serializers to work

    :param sites_data:
    :raises ValidationError:
    :return list of validated Site objects:
    """
    sites = []
    for site_data_item in sites_data:
        try:
            site = Site.objects.get(url=site_data_item['url'])
            if site.name != site_data_item['name']:
                raise serializers.ValidationError(
                    "Site failed to pass validation: different site with identical name found")
        except ObjectDoesNotExist:
            pass

        site, _ = Site.objects.get_or_create(name=site_data_item['name'],
                                             url=site_data_item['url'])
        sites.append(site)

    return sites


def process_labels(labels_data):
    """
    Return a list of labels, if any, that were pre-existing or will be created.

    :param label_data:
    :return list of Labels objects:
    """

    labels = []
    for label_item in labels_data:
        label, _ = Labels.objects.get_or_create(name=label_item['name'])
        labels.append(label)

    return labels
