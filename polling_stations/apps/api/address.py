import urllib

from addressbase.models import Address
from data_finder.helpers import (
    PostcodeError,
    geocode_point_only,
)
from data_finder.helpers.baked_data_helper import LocalParquetElectionsHelper
from data_finder.helpers.every_election import EEFetcher, EEWrapper
from data_finder.views import LogLookUpMixin, polling_station_current
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    extend_schema,
    extend_schema_field,
)
from pollingstations.models import AdvanceVotingStation
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from uk_geo_utils.helpers import Postcode

from .councils import CouncilDataSerializer, tmp_fix_parl_24_scotland_details
from .fields import PointField
from .mixins import parse_qs_to_python
from .pollingstations import PollingStationGeoSerializer


def get_bug_report_url(request, station_known):
    if not station_known:
        return None
    return request.build_absolute_uri(
        "/report_problem/?"
        + urllib.parse.urlencode({"source": "api", "source_url": request.path})
    )


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    council = serializers.CharField(source="council_name")
    polling_station_id = serializers.CharField()

    class Meta:
        model = Address
        extra_kwargs = {"url": {"view_name": "address-detail", "lookup_field": "uprn"}}

        fields = ("url", "address", "postcode", "council", "polling_station_id", "uprn")


class AdvanceVotingStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvanceVotingStation
        fields = ("name", "address", "postcode", "location", "opening_times")

    opening_times = serializers.SerializerMethodField()

    @extend_schema_field(
        {
            "type": "array",
            "example": [
                ["2022-05-03", "08:00", "16:00"],
                ["2022-05-04", "08:00", "16:00"],
            ],
        }
    )
    def get_opening_times(self, obj: AdvanceVotingStation):
        #
        return obj.opening_times_table


class BallotSerializer(serializers.Serializer):
    ballot_paper_id = serializers.SerializerMethodField()
    ballot_title = serializers.SerializerMethodField()
    poll_open_date = serializers.CharField(read_only=True)
    elected_role = serializers.CharField(read_only=True, allow_null=True)
    metadata = serializers.DictField(read_only=True, allow_null=True)
    cancelled = serializers.BooleanField(read_only=True)
    cancellation_reason = serializers.CharField(read_only=True, allow_null=True)
    replaced_by = serializers.CharField(read_only=True, allow_null=True)
    replaces = serializers.CharField(read_only=True, allow_null=True)
    requires_voter_id = serializers.CharField(read_only=True, allow_null=True)

    @extend_schema_field(OpenApiTypes.STR)
    def get_ballot_paper_id(self, obj) -> str:
        return obj["election_id"]

    @extend_schema_field(OpenApiTypes.STR)
    def get_ballot_title(self, obj) -> str:
        return obj["election_title"]


class PostcodeResponseSerializer(serializers.Serializer):
    polling_station_known = serializers.BooleanField(
        read_only=True, help_text="Do we know where this user should vote?"
    )
    postcode_location = PointField(
        read_only=True,
        help_text="A GeoJSON Feature containing a Point object describing the centroid of the input postcode.",
    )
    advance_voting_station = AdvanceVotingStationSerializer(read_only=True)
    council = CouncilDataSerializer(read_only=True)
    polling_station = PollingStationGeoSerializer(
        read_only=True, allow_null=True, help_text="A GeoJSON polling station feature"
    )
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

    def get_ee_wrapper(self, address, query_params):
        query_params = parse_qs_to_python(query_params)
        include_current = any(query_params.get("include_current", []))

        if getattr(settings, "USE_LOCAL_PARQUET_ELECTIONS", False):
            helper = LocalParquetElectionsHelper()
            resp = helper.get_response(Postcode(address.postcode), address.uprn)
            if not resp["request_success"]:
                raise APIException("failed to get list of ballots")
            return EEWrapper(
                resp["ballots"],
                request_success=resp["request_success"],
                include_current=include_current,
            )

        ee_response = EEFetcher(point=address.location).fetch()
        if not ee_response["request_success"]:
            raise APIException("failed to get list of ballots")
        return EEWrapper(**ee_response, include_current=include_current)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uprn",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="A Valid UK UPRN",
                examples=[
                    OpenApiExample(
                        "Example 1", summary="Ampthill Fish Shop", value="100080051217"
                    ),
                ],
            )
        ]
    )
    def retrieve(
        self, request, uprn=None, format=None, geocoder=geocode_point_only, log=True
    ):
        ret = {}

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
        ret["advance_voting_station"] = address.uprntocouncil.advance_voting_station

        # attempt to attach point
        # in this situation, failure to geocode is non-fatal
        try:
            geocoded_postcode = geocoder(address.postcode)
            location = geocoded_postcode.centroid
        except PostcodeError:
            location = None
        ret["postcode_location"] = location

        ret["polling_station_known"] = False
        ret["polling_station"] = None
        ee = self.get_ee_wrapper(address, request.query_params)
        has_election = ee.has_election()
        ret["council"] = tmp_fix_parl_24_scotland_details(ret["council"], ee)

        # An address might have an election but we might not know the polling station.
        if has_election and address.polling_station_id:
            # get polling station if there is an election in this area
            polling_station = address.polling_station_with_elections()
            if polling_station and polling_station_current(polling_station):
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
        log_data["location"] = address.location
        log_data["council"] = ret["council"]
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
