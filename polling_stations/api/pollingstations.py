from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from pollingstations.models import PollingStation
from .fields import PointField


class PollingStationDataSerializer(HyperlinkedModelSerializer):

    location = PointField()

    class Meta:
        model = PollingStation
        fields = ('council', 'postcode', 'address', 'location')


class PollingStationGeoSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = PollingStation
        geo_field = 'location'
        fields = ('council', 'postcode', 'address', 'location')


class PollingStationViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'head', 'options']
    queryset = PollingStation.objects.all()
    serializer_class = PollingStationDataSerializer
