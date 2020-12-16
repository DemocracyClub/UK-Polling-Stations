import urllib
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.core.exceptions import ObjectDoesNotExist

from addressbase.models import Address
from data_finder.views import LogLookUpMixin
from data_finder.helpers import (
    EveryElectionWrapper,
    geocode_point_only,
    PostcodeError,
    RoutingHelper,
)
from uk_geo_utils.helpers import Postcode
from .councils import CouncilDataSerializer
from .fields import PointField
from .pollingstations import PollingStationGeoSerializer


def get_bug_report_url(request, station_known):
    if not station_known:
        return None
    return request.build_absolute_uri(
        "/report_problem/?"
        + urllib.parse.urlencode({"source": "api", "source_url": request.path})
    )


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    council = serializers.CharField()
    polling_station_id = serializers.CharField()

    class Meta:
        model = Address
        extra_kwargs = {"url": {"view_name": "address-detail", "lookup_field": "uprn"}}

        fields = ("url", "address", "postcode", "council", "polling_station_id", "uprn")


class BallotSerializer(serializers.Serializer):
    ballot_paper_id = serializers.SerializerMethodField()
    ballot_title = serializers.SerializerMethodField()
    poll_open_date = serializers.CharField(read_only=True)
    elected_role = serializers.CharField(read_only=True, allow_null=True)
    metadata = serializers.DictField(read_only=True, allow_null=True)
    cancelled = serializers.BooleanField(read_only=True)
    replaced_by = serializers.CharField(read_only=True, allow_null=True)
    replaces = serializers.CharField(read_only=True, allow_null=True)

    def get_ballot_paper_id(self, obj):
        return obj["election_id"]

    def get_ballot_title(self, obj):
        return obj["election_title"]


class PostcodeResponseSerializer(serializers.Serializer):
    polling_station_known = serializers.BooleanField(read_only=True)
    postcode_location = PointField(read_only=True)
    custom_finder = serializers.CharField(read_only=True)
    council = CouncilDataSerializer(read_only=True)
    polling_station = PollingStationGeoSerializer(read_only=True)
    addresses = AddressSerializer(read_only=True, many=True)
    report_problem_url = serializers.CharField(read_only=True)
    metadata = serializers.DictField(read_only=True)
    ballots = BallotSerializer(read_only=True, many=True)


class AddressViewSet(ViewSet, LogLookUpMixin):

    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "post", "head", "options"]
    lookup_field = "uprn"
    serializer_class = PostcodeResponseSerializer

    def get_object(self, **kwargs):
        assert "uprn" in kwargs
        return Address.objects.get(uprn=kwargs["uprn"])

    def get_ee_wrapper(self, address):
        rh = RoutingHelper(address.postcode)
        if not rh.addresses_have_single_station:
            if address.location:
                return EveryElectionWrapper(point=address.location)
        return EveryElectionWrapper(postcode=address.postcode)

    def retrieve(
        self, request, uprn=None, format=None, geocoder=geocode_point_only, log=True
    ):
        ret = {}
        ret["custom_finder"] = None

        # attempt to get address based on uprn
        # if we fail, return an error response
        try:
            address = self.get_object(uprn=uprn)
        except ObjectDoesNotExist:
            return Response({"detail": "Address not found"}, status=404)

        # create singleton list for consistency with /postcode endpoint
        ret["addresses"] = [address]

        # council object
        ret["council"] = address.council

        # attempt to attach point
        # in this situation, failure to geocode is non-fatal
        try:
            l = geocoder(address.postcode)
            location = l.centroid
        except PostcodeError:
            location = None
        ret["postcode_location"] = location

        ret["polling_station_known"] = False
        ret["polling_station"] = None

        ee = self.get_ee_wrapper(address)
        has_election = ee.has_election()
        if has_election:
            # get polling station if there is an election in this area
            polling_station = PollingStation.objects.get_polling_station_by_id(
                address.polling_station_id, address.council_id
            )
            if polling_station:
                ret["polling_station"] = polling_station
                ret["polling_station_known"] = True

        ret["metadata"] = ee.get_metadata()

        if request.query_params.get("all_future_ballots", None):
            ret["ballots"] = ee.get_all_ballots()
        else:
            ret["ballots"] = ee.get_ballots_for_next_date()

        # create log entry
        log_data = {}
        log_data["we_know_where_you_should_vote"] = ret["polling_station_known"]
        log_data["location"] = location
        log_data["council"] = address.council
        log_data["brand"] = "api"
        log_data["language"] = ""
        log_data["api_user"] = request.user
        log_data["has_election"] = has_election
        if log:
            self.log_postcode(Postcode(address.postcode), log_data, "api")

        ret["report_problem_url"] = get_bug_report_url(
            request, ret["polling_station_known"]
        )

        serializer = PostcodeResponseSerializer(
            ret, read_only=True, context={"request": request}
        )
        return Response(serializer.data)
