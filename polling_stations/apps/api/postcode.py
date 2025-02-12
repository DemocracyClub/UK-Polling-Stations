from data_finder.helpers import (
    PostcodeError,
    RoutingHelper,
    geocode,
    get_council,
)
from data_finder.helpers.every_election import (
    EmptyEveryElectionWrapper,
)
from data_finder.views import LogLookUpMixin, polling_station_current
from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from uk_geo_utils.helpers import AddressSorter, Postcode

from .address import PostcodeResponseSerializer, get_bug_report_url
from .councils import tmp_fix_parl_24_scotland_details
from .mixins import parse_qs_to_python


class PostcodeViewSet(ViewSet, LogLookUpMixin):
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "post", "head", "options"]
    lookup_field = "postcode"
    serializer_class = PostcodeResponseSerializer

    def generate_addresses(self, routing_helper):
        if routing_helper.route_type == "multiple_addresses":
            sorter = AddressSorter(routing_helper.addresses)
            return sorter.natural_sort()
        return []

    def generate_polling_station(self, routing_helper):
        if routing_helper.route_type == "single_address":
            return routing_helper.addresses[0].polling_station_with_elections()
        return None

    def generate_advance_voting_station(self, routing_helper):
        if routing_helper.route_type == "single_address":
            return routing_helper.addresses[0].uprntocouncil.advance_voting_station
        return None

    def get_ee_wrapper(self, postcode, rh, query_params):
        if rh.route_type == "multiple_addresses":
            return EmptyEveryElectionWrapper()
        if rh.elections_response:
            return rh.elections_backend.ee_wrapper(rh.elections_response)
        kwargs = {}
        query_params = parse_qs_to_python(query_params)
        if include_current := query_params.get("include_current", False):
            kwargs["include_current"] = any(include_current)
        return rh.elections_backend.ee_wrapper(postcode, **kwargs)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="postcode",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="A Valid UK postcode",
                examples=[
                    OpenApiExample(
                        "Example 1", summary="Buckingham Palace", value="SW1A 1AA"
                    ),
                ],
            )
        ]
    )
    def retrieve(self, request, postcode=None, format=None, geocoder=geocode, log=True):
        postcode = Postcode(postcode)
        ret = {}

        rh = RoutingHelper(postcode)

        # attempt to attach point and gss_codes
        try:
            loc = geocoder(postcode)
            location = loc.centroid
        except PostcodeError as e:
            return Response({"detail": e.args[0]}, status=400)

        ret["postcode_location"] = location

        # council object
        if rh.councils or not loc:
            # We can't assign this postcode to exactly one council
            council = None
        else:
            try:
                council = get_council(loc)
            except ObjectDoesNotExist:
                return Response({"detail": "Internal server error"}, 500)
        ret["council"] = council

        ret["addresses"] = self.generate_addresses(rh)

        ret["polling_station_known"] = False
        ret["polling_station"] = None

        ee = self.get_ee_wrapper(postcode, rh, request.query_params)
        has_election = ee.has_election()
        if has_election:
            ret["council"] = tmp_fix_parl_24_scotland_details(ret["council"], ee)

            # get polling station if there is an election in this area
            ret["polling_station_known"] = False
            ret["polling_station"] = self.generate_polling_station(rh)
            if ret["polling_station"]:
                if polling_station_current(ret["polling_station"]):
                    ret["polling_station_known"] = True
                else:
                    ret["polling_station"] = None
            if ret["polling_station"] and not ret["council"]:
                ret["council"] = ret["polling_station"].council

        # get advance voting station
        ret["advance_voting_station"] = self.generate_advance_voting_station(rh)

        ret["metadata"] = ee.get_metadata()

        if request.query_params.get("all_future_ballots", None):
            ret["ballots"] = ee.get_all_ballots()
        else:
            ret["ballots"] = ee.get_ballots_for_next_date()

        # create log entry
        log_data = {}
        log_data["we_know_where_you_should_vote"] = ret["polling_station_known"]
        log_data["location"] = location
        log_data["council"] = council
        log_data["brand"] = "api"
        log_data["language"] = ""
        log_data["api_user"] = request.user
        log_data["has_election"] = has_election
        if log and not ret["addresses"]:
            self.log_postcode(postcode, log_data, "api")
            # don't log 'address select' hits

        ret["report_problem_url"] = get_bug_report_url(
            request, ret["polling_station_known"]
        )

        serializer = PostcodeResponseSerializer(
            ret, read_only=True, context={"request": request}
        )
        return Response(serializer.data)
