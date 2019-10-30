from urllib.parse import urlencode

from django.urls import reverse
from django.utils.functional import cached_property
from uk_geo_utils.helpers import Postcode

from addressbase.models import Blacklist
from pollingstations.models import ResidentialAddress


# use a postcode to decide which endpoint the user should be directed to
class RoutingHelper:
    _query_params_to_preserve = {
        "utm_content",
        "utm_medium",
        "utm_source",
        "utm_campaign",
    }

    def __init__(self, postcode):
        self.postcode = Postcode(postcode).without_space
        self.get_addresses()
        self.get_councils_from_blacklist()

    def get_addresses(self):
        self.addresses = ResidentialAddress.objects.filter(postcode=self.postcode)
        return self.addresses

    def get_councils_from_blacklist(self):
        # if this postcode appears in the blacklist table
        # return a list of any council ids attached to it
        # if it is not in the table, we will return []
        blacklist = Blacklist.objects.filter(postcode=self.postcode)
        self.councils = [row.lad for row in blacklist]
        return self.councils

    @property
    def has_addresses(self):
        return bool(self.addresses)

    @property
    def has_single_address(self):
        return self.addresses.count == 1

    @property
    def address_have_single_station(self):
        stations = self.addresses.values("polling_station_id").distinct()
        return len(stations) == 1

    @property
    def route_type(self):
        if len(self.councils) > 1:
            return "multiple_councils"
        if self.has_addresses:
            if self.address_have_single_station:
                # all the addresses in this postcode
                # map to one polling station
                return "single_address"
            else:
                # addresses in this postcode map to
                # multiple polling stations
                return "multiple_addresses"
        else:
            # postcode is not in ResidentialAddress table
            return "postcode"

    @cached_property
    def view(self):
        if self.route_type == "multiple_councils":
            # this postcode contains UPRNS situated in >1 local auth
            # maybe one day we will handle this better, but for now
            # we just throw a special "we don't know" page
            # ..even if we might possibly know
            return "multiple_councils_view"
        if self.route_type == "single_address":
            # all the addresses in this postcode
            # map to one polling station
            return "address_view"
        if self.route_type == "multiple_addresses":
            # addresses in this postcode map to
            # multiple polling stations
            return "address_select_view"
        if self.route_type == "postcode":
            # postcode is not in ResidentialAddress table
            return "postcode_view"

    @cached_property
    def kwargs(self):
        if self.route_type in ("multiple_councils", "multiple_addresses", "postcode"):
            return {"postcode": self.postcode}
        if self.route_type in {"single_address"}:
            return {"address_slug": self.addresses[0].slug}

    def get_canonical_url(self, request, preserve_query=True):
        """Returns a canonical URL to route to, preserving any important query parameters"""
        url = reverse(self.view, kwargs=self.kwargs)
        query = urlencode(
            [
                (k, request.GET.getlist(k))
                for k in request.GET
                if k in self._query_params_to_preserve
            ],
            doseq=True,
        )
        if query and preserve_query:
            url += "?" + query
        return url
