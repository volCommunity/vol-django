from vol.models import Labels, Organisation, Site, Job

from rest_framework import serializers


class LabelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Labels
        fields = ['id', 'name', 'created_at', 'updated_at']


class OrganisationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Organisation
        fields = ('id', 'name', 'region', 'city', 'url', 'created_at', 'updated_at')


class SiteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Site
        fields = ('id', 'name', 'url', 'created_at', 'updated_at')


class JobSerializer(serializers.HyperlinkedModelSerializer):
    """
    Allows GETting and POSTing of jobs, but will display labels and site flat
    ie:
    ▶ curl -X GET http://localhost:8000/api/v0.0.1/jobs/4
        {"id":4,"title":"Nappy changer",
        "text":"This is a great opportunity for young and old",
        "labels":[5],"organisation":{"id":1,
        "name":"Volunteer Wellington","region":"wellington","city":"wellington",
        "url":"https://www.volunteerwellington.org.nz/","added":"2017-09-19"},
        "sites":[2],"country":"new zealand","region":"otago","added":"2017-09-19",
        "url":"https://dogoodjobs.co.nz/nappy-changer","seen":0}

        While we want to expand sites and labels, looking like so:
        {"id":4,"title":"Nappy changer",
        "text":"This is a great opportunity for young and old",
        "labels":[{"id":5,"name":"people"}],"organisation":{"id":1,
            "name":"Volunteer Wellington",
            "region":"wellington",
            "city":"wellington",
            "url":"https://www.volunteerwellington.org.nz/",
            "added":"2017-09-19"},
        "sites":[{"id":2,
            "name":"Do Good Jobs",
            "url":"https://dogoodjobs.co.nz",
            "added":"2017-07-03"}],
        "country":"new zealand","region":"otago","added":"2017-09-19",
        "url":"https://dogoodjobs.co.nz/nappy-changer","seen":0}

    The challenge is to use `LabelSerializer(read_only=True, many=True)` for reads and
    `serializers.PrimaryKeyRelatedField(
        queryset=Labels.objects.all(), many=True)` for updates.
    """
    organisation = OrganisationSerializer(read_only=True)

    labels = serializers.PrimaryKeyRelatedField(
        queryset=Labels.objects.all(), many=True)
    sites = serializers.PrimaryKeyRelatedField(
        queryset=Site.objects.all(), many=True)

    organisation_id = serializers.PrimaryKeyRelatedField(
        queryset=Organisation.objects.all(), source='organisation', write_only=True)

    class Meta:
        model = Job
        fields = ('id', 'title', 'text', 'labels', 'organisation_id', 'organisation',
                  'sites', 'country', 'region', 'created_at', 'updated_at', 'url', 'seen')
