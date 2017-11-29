from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.core.exceptions import ObjectDoesNotExist
from councils.models import Council
from data_finder.views import LogLookUpMixin
from data_finder.helpers import (
    get_council,
    geocode,
    PostcodeError,
    MultipleCouncilsException,
    RoutingHelper
)
from pollingstations.models import PollingStation, CustomFinder
from uk_geo_utils.helpers import AddressSorter, Postcode
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
            sorter = AddressSorter(routing_helper.addresses)
            return sorter.natural_sort()
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

    def generate_custom_finder(self, geocoder, postcode):
        finder = CustomFinder.objects.get_custom_finder(geocoder, postcode)
        if finder and finder.base_url:
            if finder.can_pass_postcode:
                return finder.base_url + finder.encoded_postcode
            else:
                return finder.base_url
        else:
            return None

    def retrieve(self, request, postcode=None, format=None, geocoder=geocode, log=True):
        postcode = Postcode(postcode)
        ret = {}

        # attempt to attach point and gss_codes
        # in this situation, failure to geocode is fatal
        # (we need codes to pass to get_custom_finder)
        try:
            loc = geocoder(postcode)
            location = loc.centroid
        except PostcodeError as e:
            return Response({'detail': e.args[0]}, status=400)
        except MultipleCouncilsException as e:
            loc = None
            location = None

        ret['postcode_location'] = location

        rh = RoutingHelper(postcode)

        # council object
        if rh.route_type == "multiple_councils":
            # We can't assign this postcode to exactly one council
            council = None
        else:
            try:
                council = get_council(loc)
            except ObjectDoesNotExist:
                return Response({'detail': 'Internal server error'}, 500)
        ret['council'] = council

        ret['addresses'] = self.generate_addresses(rh)

        # get polling station
        ret['polling_station_known'] = False
        ret['polling_station'] = self.generate_polling_station(rh, council, location)
        if ret['polling_station']:
            ret['polling_station_known'] = True

        # get custom finder (if no polling station)
        ret['custom_finder'] = None
        if not ret['polling_station_known'] and loc:
            ret['custom_finder'] = self.generate_custom_finder(loc, postcode)

        # create log entry
        log_data = {}
        log_data['we_know_where_you_should_vote'] = ret['polling_station_known']
        log_data['location'] = location
        log_data['council'] = council
        log_data['brand'] = 'api'
        log_data['language'] = ''
        log_data['api_user'] = request.user
        if log:
            if not ret['addresses']:
                self.log_postcode(postcode, log_data, 'api')
            # don't log 'address select' hits

        serializer = PostcodeResponseSerializer(
            ret, read_only=True, context={'request': request}
        )
        return Response(serializer.data)
