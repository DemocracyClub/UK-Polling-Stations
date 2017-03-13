from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.contrib.gis.geos import Point
from django.core.exceptions import ObjectDoesNotExist
from councils.models import Council
from data_finder.views import LogLookUpMixin
from data_finder.helpers import (
    geocode,
    PostcodeError,
    RateLimitError,
    RoutingHelper
)
from pollingstations.models import PollingStation, CustomFinder
from .address import PostcodeResponseSerializer


class PostcodeViewSet(ViewSet, LogLookUpMixin):

    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'head', 'options']
    lookup_field = 'postcode'
    serializer_class = PostcodeResponseSerializer

    def get_object(self, **kwargs):
        assert 'location' in kwargs
        assert 'council' in kwargs
        return PollingStation.objects.get_polling_station(
            kwargs['council'],
            location=kwargs['location']
        )

    def generate_addresses(self, routing_helper):
        if routing_helper.route_type == "multiple_addresses":
            return [address for address in routing_helper.addresses]
        return []

    def generate_polling_station(self, routing_helper, council, location):
        if routing_helper.route_type == "single_address":
            return PollingStation.objects.get_polling_station_by_id(
                routing_helper.addresses[0].polling_station_id,
                council_id=routing_helper.addresses[0].council_id
            )
        elif routing_helper.route_type == "postcode":
            return self.get_object(
                location=location,
                council=council,
            )
        else:
            return None

    def generate_custom_finder(self, gss_codes, postcode):
        finder = CustomFinder.objects.get_custom_finder(gss_codes, postcode)
        if finder and finder.base_url:
            if finder.can_pass_postcode:
                return finder.base_url + finder.encoded_postcode
            else:
                return finder.base_url
        else:
            return None

    def retrieve(self, request, postcode=None, format=None, geocoder=geocode, log=True):
        postcode = postcode.replace(' ', '')
        ret = {}

        # attempt to attach point and gss_codes
        # in this situation, failure to geocode is fatal
        # (we need 'gss_codes' to pass to get_custom_finder)
        try:
            l = geocoder(postcode)
        except PostcodeError as e:
            return Response({'detail': e.args[0]}, status=400)
        except RateLimitError as e:
            return Response({'detail': e.args[0]}, status=403)

        location = Point(l['wgs84_lon'], l['wgs84_lat'])
        ret['postcode_location'] = location

        # council object
        try:
            council = Council.objects.get(area__covers=location)
        except ObjectDoesNotExist:
            if postcode[:2] == 'BT' or 'N07000001' in l['gss_codes']:
                # this postcode is in Northern Ireland
                ret['polling_station_known'] = False
                ret['council'] = None
                ret['polling_station'] = None
                ret['custom_finder'] = self.generate_custom_finder(l['gss_codes'], postcode)
                ret['addresses'] = []
                serializer = PostcodeResponseSerializer(
                    ret, read_only=True, context={'request': request}
                )
                return Response(serializer.data)
            else:
                return Response({'detail': 'Internal server error'}, 500)
        ret['council'] = council

        rh = RoutingHelper(postcode)

        ret['addresses'] = self.generate_addresses(rh)

        # get polling station
        ret['polling_station_known'] = False
        ret['polling_station'] = self.generate_polling_station(rh, council, location)
        if ret['polling_station']:
            ret['polling_station_known'] = True

        # get custom finder (if no polling station)
        ret['custom_finder'] = None
        if not ret['polling_station_known']:
            ret['custom_finder'] = self.generate_custom_finder(l['gss_codes'], postcode)

        # create log entry
        log_data = {}
        log_data['we_know_where_you_should_vote'] = ret['polling_station_known']
        log_data['location'] = location
        log_data['council'] = council
        log_data['brand'] = 'api'
        log_data['language'] = ''
        if log:
            self.log_postcode(postcode, log_data, 'api')

        serializer = PostcodeResponseSerializer(
            ret, read_only=True, context={'request': request}
        )
        return Response(serializer.data)
