from rest_framework.decorators import list_route
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.serializers import CharField, HyperlinkedModelSerializer
from rest_framework.viewsets import GenericViewSet
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from pollingstations.models import PollingStation


class PollingStationDataSerializer(HyperlinkedModelSerializer):

    station_id = CharField(source='internal_council_id', read_only=True)

    class Meta:
        model = PollingStation
        fields = ('council', 'station_id', 'postcode', 'address')


class PollingStationGeoSerializer(GeoFeatureModelSerializer):

    station_id = CharField(source='internal_council_id', read_only=True)

    class Meta:
        model = PollingStation
        geo_field = 'location'
        fields = ('council', 'station_id', 'postcode', 'address', 'location')


class PollingStationViewSet(GenericViewSet, ListModelMixin):
    queryset = PollingStation.objects.all()

    def get_queryset(self):
        council_id = self.request.query_params.get('council_id', None)
        station_id = self.request.query_params.get('station_id', None)

        if council_id is None:
            return PollingStation.objects.all()

        if station_id is None:
            return PollingStation.objects.filter(council=council_id)

        return PollingStation.objects.filter(
            council=council_id, internal_council_id=station_id)

    def validate_request(self):
        if 'station_id' in self.request.query_params and\
            'council_id' not in self.request.query_params:
                return False
        return True

    def list(self, request, *args, **kwargs):
        if not self.validate_request():
            return Response(
                {'detail': 'council_id parameter must be specified'}, 400)

        queryset = self.get_queryset()
        serializer = PollingStationDataSerializer(
            queryset, many=True, read_only=True, context={'request': request})
        return Response(serializer.data)

    @list_route(url_path='geo')
    def geo(self, request, format=None):
        if not self.validate_request():
            return Response(
                {'detail': 'council_id parameter must be specified'}, 400)

        queryset = self.get_queryset()
        serializer = PollingStationGeoSerializer(
            queryset, many=True, read_only=True, context={'request': request})
        return Response(serializer.data)
