from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from councils.models import Council
from data_finder.views import LogLookUpMixin
from data_finder.helpers import (
    geocode,
    PostcodeError,
    RateLimitError,
    RoutingHelper
)
from pollingstations.models import PollingStation, CustomFinder
from .address import ResidentialAddressSerializer
from .councils import CouncilDataSerializer as CouncilSerializer
from .fields import PointField
from .pollingstations import PollingStationDataSerializer as PollingStationSerializer


class PostcodeViewSet(viewsets.ViewSet, LogLookUpMixin):

    http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self, **kwargs):
        if not kwargs:
            return PollingStation.objects.all()
        assert 'location' in kwargs
        assert 'council' in kwargs
        return PollingStation.objects.get_polling_station(
            kwargs['council']['council_id'],
            location=kwargs['location']
        )

    def retrieve(self, request, pk=None, format=None):
        postcode = pk.replace(' ', '')
        ret = {}
        ret['polling_station_known'] = False
        polling_station = None

        try:
            l = geocode(pk)
        except PostcodeError as e:
            ret['error'] = e.args[0]
            return Response(ret, status=400)
        except RateLimitError as e:
            ret['error'] = e.args[0]
            return Response(ret, status=403)

        location = Point(l['wgs84_lon'], l['wgs84_lat'])
        ret['postcode_location'] = PointField().to_representation(location)

        council = Council.objects.get(area__covers=location)
        ret['council'] = CouncilSerializer(council).data

        rh = RoutingHelper(postcode)

        ret['addresses'] = []
        if rh.route_type == "multiple_addresses":
            ret['addresses'] = [
                ResidentialAddressSerializer(address, context={
                    'request': self.request}
                    ).data for address in
                rh.addresses
            ]

        if rh.route_type == "single_address":
            polling_station = PollingStation.objects.get_polling_station_by_id(
                rh.addresses[0].polling_station_id,
                council_id=rh.addresses[0].council_id
                )

        if rh.route_type == "postcode":
            polling_station = self.get_queryset(
                location=location,
                council=ret['council'],
                )

        ret['polling_station'] = None
        if polling_station:
            ret['polling_station_known'] = True
            ret['polling_station'] = PollingStationSerializer(
                polling_station, context={'request': self.request}).data

        ret['custom_finder'] = None
        if not ret['polling_station_known']:
            finder = CustomFinder.objects.get_custom_finder(l['gss_codes'], postcode)
            if finder and finder.base_url:
                ret['custom_finder'] = {}
                ret['custom_finder']['base_url'] = finder.base_url
                ret['custom_finder']['can_pass_postcode'] = finder.can_pass_postcode
                ret['custom_finder']['encoded_postcode'] = finder.encoded_postcode

        log_data = {}
        log_data['we_know_where_you_should_vote'] = ret['polling_station_known']
        log_data['location'] = location
        log_data['council'] = council
        log_data['brand'] = 'api'
        log_data['language'] = ''
        self.log_postcode(postcode, log_data, 'api')

        return Response(ret)
