from rest_framework import serializers, viewsets
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.core.exceptions import ObjectDoesNotExist
from data_finder.views import LogLookUpMixin
from data_finder.helpers import (
    geocode_point_only,
    PostcodeError,
    RateLimitError,
)
from pollingstations.models import PollingStation, ResidentialAddress
from .councils import CouncilDataSerializer as CouncilSerializer
from .fields import PointField
from .pollingstations import PollingStationDataSerializer as PollingStationSerializer


class ResidentialAddressSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ResidentialAddress
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'view_name': 'address-detail', 'lookup_field': 'slug'}
        }

        fields = ('url', 'address', 'postcode', 'council', 'polling_station_id')


class ResidentialAddressViewSet(viewsets.ViewSet, LogLookUpMixin):

    http_method_names = ['get', 'post', 'head', 'options']
    lookup_field = 'slug'

    def get_queryset(self, **kwargs):
        if not kwargs:
            return ResidentialAddress.objects.all()
        assert 'slug' in kwargs
        return ResidentialAddress.objects.get(slug=kwargs['slug'])

    def retrieve(self, request, slug=None, format=None):
        ret = {}
        ret['custom_finder'] = None

        # attempt to get address based on slug
        # if we fail, return an error response
        try:
            address = self.get_queryset(slug=slug)
        except ObjectDoesNotExist as e:
            return Response({'detail': 'Address not found'}, status=404)

        # create singleton list for consistency with /postcode endpoint
        ret['addresses'] = [
            ResidentialAddressSerializer(
                address,
                context={'request': self.request}
            ).data
        ]

        ret['council'] = CouncilSerializer(
            address.council, context={'request': request}).data

        # attempt to attach point
        # in this situation, failure to geocode is non-fatal
        try:
            l = geocode_point_only(address.postcode)
            location = Point(l['wgs84_lon'], l['wgs84_lat'])
            ret['postcode_location'] = PointField().to_representation(location)
        except (PostcodeError, RateLimitError) as e:
            location = None
            ret['postcode_location'] = None

        # get polling station
        polling_station = PollingStation.objects.get_polling_station_by_id(
            address.polling_station_id, address.council_id)
        ret['polling_station_known'] = False
        ret['polling_station'] = None
        if polling_station:
            ret['polling_station'] = PollingStationSerializer(
                polling_station, context={'request': self.request}).data
            ret['polling_station_known'] = True

        # create log entry
        log_data = {}
        log_data['we_know_where_you_should_vote'] = ret['polling_station_known']
        log_data['location'] = location
        log_data['council'] = address.council
        log_data['brand'] = 'api'
        log_data['language'] = ''
        self.log_postcode(address.postcode, log_data, 'api')

        return Response(ret)
