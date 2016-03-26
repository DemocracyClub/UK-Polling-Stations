"""
Polling Stations Open Data API
"""

from django.utils.encoding import smart_str
from rest_framework import routers, serializers, viewsets, views
from councils.models import Council
from pollingstations.models import (PollingStation, PollingDistrict,
    ResidentialAddress)

# Fields define serialization of complex field types (GEO)
class PointField(serializers.Field):
    type_name = 'PointField'
    type_label = 'point'

    def to_representation(self, value):
        """
        Transform POINT object to json.
        """
        if value is None:
            return value

        value = {
            "latitude": smart_str(value.y),
            "longitude": smart_str(value.x)
        }
        return value


class PolygonField(serializers.Field):
    type_name = 'PolygonField'
    type_label = 'polygon'

    def to_representation(self, value):
        if value is None:
            return value
        return value.coords


# Serializers define the API representation.
class CouncilSerializer(serializers.HyperlinkedModelSerializer):
    location = PointField()
#    area = PolygonField()
    class Meta:
        model = Council
        fields = (
            'council_id', 'council_type', 'mapit_id', 'name',
            'email', 'phone', 'website', 'postcode', 'address',
            'location',
#            'area' # This is super slow ATM - TODO!
        )


class PollingStationSerializer(serializers.HyperlinkedModelSerializer):
    location = PointField()
    class Meta:
        model = PollingStation
        fields = ('council', 'postcode', 'address', 'location')


class ResidentialAddressSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ResidentialAddress
        fields = ('address','postcode','council','polling_station_id')


class PollingDistrictSerializer(serializers.HyperlinkedModelSerializer):
    # area = PolygonField()
    class Meta:
        model = PollingDistrict
        fields = (
            'name', 'council',
#            'area' This is super slow ATM TODO!
        )


# ViewSets define the view behavior.
class CouncilViewSet(viewsets.ModelViewSet):
    queryset = Council.objects.all()
    serializer_class = CouncilSerializer


class PollingStationViewSet(viewsets.ModelViewSet):
    queryset = PollingStation.objects.all()
    serializer_class = PollingStationSerializer


class PollingDistrictViewSet(viewsets.ModelViewSet):
    queryset = PollingDistrict.objects.all()
    serializer_class = PollingDistrictSerializer

from rest_framework.response import Response
from data_finder.helpers import PostcodeError, geocode, RoutingHelper
from django.contrib.gis.geos import Point


class PostcodeViewSet(viewsets.ViewSet):
    def get_queryset(self, **kwargs):
        if not kwargs:
            return PollingStation.objects.all()
        assert 'location' in kwargs
        assert 'council' in kwargs
        return PollingStation.objects.get_polling_station(
            kwargs['location'],
            kwargs['council']['council_id']
        )

    def retrieve(self, requst, pk=None, format=None):
        postcode = pk.replace(' ', '')
        ret = {}
        ret['polling_station_known'] = False
        polling_station = None

        try:
            l = geocode(pk)
        except PostcodeError as e:
            ret['error'] = e.args[0]
            return Response(ret)

        location = Point(l['wgs84_lon'], l['wgs84_lat'])
        ret['postcode_location'] = PointField().to_representation(
            location)

        ret['council'] = CouncilSerializer(Council.objects.get(
            area__covers=location)).data

        rh = RoutingHelper(postcode)

        if rh.route_type == "multiple_addresses":
            ret['addresses'] = [
                ResidentialAddressSerializer(address, context={
                    'request': self.request}
                    ).data for address in
                rh.addresses
            ]

        if rh.route_type == "single_address":
            polling_station = rh.addresses[0]

        if rh.route_type == "postcode":
            polling_station = self.get_queryset(
                location=location,
                council=ret['council'],
                )

        if polling_station:
            ret['polling_station_known'] = True
            ret['polling_station'] = PollingStationSerializer(
                polling_station, context={'request': self.request}).data

        return Response(ret)


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'councils', CouncilViewSet)
router.register(r'pollingstations', PollingStationViewSet)
router.register(r'pollingdistricts', PollingDistrictViewSet)
router.register(r'postcode', PostcodeViewSet, base_name="postcode")
