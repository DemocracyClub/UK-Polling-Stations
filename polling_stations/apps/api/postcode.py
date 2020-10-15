from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.core.exceptions import ObjectDoesNotExist
from data_finder.views import LogLookUpMixin
from data_finder.helpers import (
    EveryElectionWrapper,
    get_council,
    geocode,
    PostcodeError,
    RoutingHelper,
)
from pollingstations.models import PollingStation, CustomFinder
from uk_geo_utils.helpers import AddressSorter, Postcode
from .address import PostcodeResponseSerializer, get_bug_report_url


class PostcodeViewSet(ViewSet, LogLookUpMixin):

    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "post", "head", "options"]
    lookup_field = "postcode"
    serializer_class = PostcodeResponseSerializer

    def get_object(self, **kwargs):
        assert "location" in kwargs
        assert "council" in kwargs
        return PollingStation.objects.get_polling_station(
            kwargs["council"], location=kwargs["location"]
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
                council_id=routing_helper.addresses[0].council,
            )
        elif routing_helper.route_type == "postcode":
            return self.get_object(location=location, council=council)
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

    def get_ee_wrapper(self, postcode):
        return EveryElectionWrapper(postcode)

    def retrieve(self, request, postcode=None, format=None, geocoder=geocode, log=True):
        postcode = Postcode(postcode)
        ret = {}
        rh = RoutingHelper(postcode)

        # attempt to attach point and gss_codes
        try:
            loc = geocoder(postcode)
            location = loc.centroid
        except PostcodeError as e:
            if rh.route_type == "single_address":
                loc = None
                location = None
            else:
                return Response({"detail": e.args[0]}, status=400)

        ret["postcode_location"] = location

        # council object
        if rh.route_type == "multiple_councils" or not loc:
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

        ee = self.get_ee_wrapper(postcode)
        has_election = ee.has_election()
        if has_election:
            # get polling station if there is an election in this area
            ret["polling_station_known"] = False
            ret["polling_station"] = self.generate_polling_station(
                rh, council, location
            )
            if ret["polling_station"]:
                ret["polling_station_known"] = True
            if ret["polling_station"] and not ret["council"]:
                ret["council"] = ret["polling_station"].council

        # get custom finder (if no polling station)
        ret["custom_finder"] = None
        if not ret["polling_station_known"] and loc:
            ret["custom_finder"] = self.generate_custom_finder(loc, postcode)

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
        if log:
            if not ret["addresses"]:
                self.log_postcode(postcode, log_data, "api")
            # don't log 'address select' hits

        ret["report_problem_url"] = get_bug_report_url(
            request, ret["polling_station_known"]
        )

        serializer = PostcodeResponseSerializer(
            ret, read_only=True, context={"request": request}
        )
        return Response(serializer.data)
