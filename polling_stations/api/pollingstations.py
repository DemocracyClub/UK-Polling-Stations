from rest_framework.decorators import list_route
from rest_framework.mixins import ListModelMixin
from rest_framework.serializers import CharField
from rest_framework.viewsets import GenericViewSet
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from pollingstations.models import PollingStation


class PollingStationSerializer(GeoFeatureModelSerializer):

    station_id = CharField(source='internal_council_id', read_only=True)

    class Meta:
        model = PollingStation
        geo_field = 'location'
        fields = ('council', 'station_id', 'postcode', 'address', 'location')


class PollingStationViewSet(GenericViewSet, ListModelMixin):
    queryset = PollingStation.objects.all()
    serializer_class = PollingStationSerializer

    @list_route(url_path='geo')
    def geo(self, request, format=None):
        return self.list(request, format=None)
