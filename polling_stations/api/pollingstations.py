from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from pollingstations.models import PollingStation


class PollingStationSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = PollingStation
        geo_field = 'location'
        fields = ('council', 'postcode', 'address', 'location')


class PollingStationViewSet(ReadOnlyModelViewSet):
    queryset = PollingStation.objects.all()
    serializer_class = PollingStationSerializer
