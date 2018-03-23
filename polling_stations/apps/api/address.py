import urllib
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.core.exceptions import ObjectDoesNotExist
from data_finder.views import LogLookUpMixin
from data_finder.helpers import (
    EveryElectionWrapper,
    geocode_point_only,
    PostcodeError,
    RoutingHelper,
)
from pollingstations.models import PollingStation, ResidentialAddress
from uk_geo_utils.helpers import Postcode
from .councils import CouncilDataSerializer
from .fields import PointField
from .pollingstations import PollingStationGeoSerializer


def get_bug_report_url(request, station_known):
    if not station_known:
        return None
    return request.build_absolute_uri(
        '/report_problem/?' + urllib.parse.urlencode({
            'source': 'api',
            'source_url': request.path,
        })
    )


class ResidentialAddressSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ResidentialAddress
        extra_kwargs = {
            'url': {'view_name': 'address-detail', 'lookup_field': 'slug'}
        }

        fields = ('url', 'address', 'postcode', 'council', 'polling_station_id')


class PostcodeResponseSerializer(serializers.Serializer):
    polling_station_known = serializers.BooleanField(read_only=True)
    postcode_location = PointField(read_only=True)
    custom_finder = serializers.CharField(read_only=True)
    council = CouncilDataSerializer(read_only=True)
    polling_station = PollingStationGeoSerializer(read_only=True)
    addresses = ResidentialAddressSerializer(read_only=True, many=True)
    report_problem_url = serializers.CharField(read_only=True)
    metadata = serializers.DictField(read_only=True)


class ResidentialAddressViewSet(ViewSet, LogLookUpMixin):

    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'head', 'options']
    lookup_field = 'slug'
    serializer_class = PostcodeResponseSerializer

    def get_object(self, **kwargs):
        assert 'slug' in kwargs
        return ResidentialAddress.objects.get(slug=kwargs['slug'])

    def get_ee_wrapper(self, address):
        rh = RoutingHelper(address.postcode)
        if not rh.address_have_single_station:
            if address.location:
                return EveryElectionWrapper(point=address.location)
        return EveryElectionWrapper(postcode=address.postcode)

    def retrieve(self, request, slug=None, format=None, geocoder=geocode_point_only, log=True):
        ret = {}
        ret['custom_finder'] = None

        # attempt to get address based on slug
        # if we fail, return an error response
        try:
            address = self.get_object(slug=slug)
        except ObjectDoesNotExist as e:
            return Response({'detail': 'Address not found'}, status=404)

        # create singleton list for consistency with /postcode endpoint
        ret['addresses'] = [address]

        # council object
        ret['council'] = address.council

        # attempt to attach point
        # in this situation, failure to geocode is non-fatal
        try:
            l = geocoder(address.postcode)
            location = l.centroid
        except PostcodeError as e:
            location = None
        ret['postcode_location'] = location

        ret['polling_station_known'] = False
        ret['polling_station'] = None

        ee = self.get_ee_wrapper(address)
        if ee.has_election():
            # get polling station if there is an election in this area
            polling_station = PollingStation.objects.get_polling_station_by_id(
                address.polling_station_id, address.council_id)
            if polling_station:
                ret['polling_station'] = polling_station
                ret['polling_station_known'] = True

        ret['metadata'] = ee.get_metadata()

        # create log entry
        log_data = {}
        log_data['we_know_where_you_should_vote'] = ret['polling_station_known']
        log_data['location'] = location
        log_data['council'] = address.council
        log_data['brand'] = 'api'
        log_data['language'] = ''
        log_data['api_user'] = request.user
        if log:
            self.log_postcode(Postcode(address.postcode), log_data, 'api')

        ret['report_problem_url'] = get_bug_report_url(request, ret['polling_station_known'])

        serializer = PostcodeResponseSerializer(
            ret, read_only=True, context={'request': request}
        )
        return Response(serializer.data)
