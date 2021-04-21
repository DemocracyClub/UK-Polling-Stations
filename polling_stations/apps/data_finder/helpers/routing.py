from urllib.parse import urlencode

from django.urls import reverse
from django.utils.functional import cached_property
from uk_geo_utils.helpers import Postcode

from addressbase.models import Address


# use a postcode to decide which endpoint the user should be directed to
from councils.models import CouncilGeography


class RoutingHelper:
    _query_params_to_preserve = {
        "utm_content",
        "utm_medium",
        "utm_source",
        "utm_campaign",
    }

    def __init__(self, postcode):
        self.postcode = Postcode(postcode)
        self.addresses = self.get_addresses()

    def get_addresses(self):
        return Address.objects.filter(postcode=self.postcode.with_space).select_related(
            "uprntocouncil"
        )

    @property
    def councils(self):
        gss_codes = {a.uprntocouncil.lad for a in self.addresses if a.uprntocouncil.lad}
        council_ids = set(
            CouncilGeography.objects.filter(gss__in=gss_codes).values_list(
                "council_id", flat=True
            )
        )

        if len(council_ids) == 1:
            return None
        else:
            return list(council_ids)

    @property
    def polling_stations(self):
        return {address.polling_station_id for address in self.addresses}

    @property
    def has_addresses(self):
        return bool(self.addresses)

    @property
    def no_stations(self):
        """Return true if there are addresses, but no polling station information"""
        return self.polling_stations == {""}

    @property
    def addresses_have_single_station(self):
        """Check if all addresses have the same polling station id and
        that it is not an empty string"""
        if len(self.polling_stations) == 1:
            return bool(list(self.polling_stations)[0])
        else:
            return False

    @property
    def route_type(self):
        if not self.has_addresses:
            # Postcode is not in addressbase
            return "postcode"
        if self.councils and self.no_stations:
            # multiple councils and no stations for any address in postcode
            return "multiple_addresses"
        if self.no_stations:
            # We don't have any station information for this address
            return "postcode"
        if self.addresses_have_single_station:
            # all the addresses in this postcode
            # map to one polling station
            return "single_address"
        else:
            # addresses in this postcode map to
            # multiple polling stations
            return "multiple_addresses"

    @cached_property
    def view(self):
        if self.route_type == "single_address":
            # all the addresses in this postcode
            # map to one polling station
            return "address_view"
        if self.route_type == "multiple_addresses":
            # addresses in this postcode map to
            # multiple polling stations
            return "address_select_view"
        if self.route_type == "postcode":
            # postcode is not in addressbase table or we
            # don't have any polling station information for it.
            return "postcode_view"

    @cached_property
    def kwargs(self):
        if self.route_type == "single_address":
            return {"uprn": self.addresses[0].uprn}
        return {"postcode": self.postcode.without_space}

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
