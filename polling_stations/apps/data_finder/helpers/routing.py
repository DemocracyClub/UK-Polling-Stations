from urllib.parse import urlencode

from addressbase.models import Address

# use a postcode to decide which endpoint the user should be directed to
from councils.models import CouncilGeography
from data_finder.helpers.baked_data_helper import (
    LocalParquetElectionsHelper,
    NoOpElectionsHelper,
)
from django.conf import settings
from django.urls import reverse
from django.utils.functional import cached_property
from uk_geo_utils.helpers import Postcode


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
        self.elections_backend = self.get_elections_backend()
        self._elections_response = None

    def get_elections_backend(self):
        if getattr(settings, "USE_LOCAL_PARQUET_ELECTIONS", False):
            return LocalParquetElectionsHelper
        return NoOpElectionsHelper

    def get_addresses(self):
        return Address.objects.filter(postcode=self.postcode.with_space).select_related(
            "uprntocouncil"
        )

    @property
    def councils(self):
        """
        This method returns None when all the addresses in the postcode are in the same council, and otherwise returns
        a list of council_ids that the postcode overlaps.

        It is also being pressed into service to set a `_council_name` property on all the address objects with the
        postcode. This means we want to call this before serializing the postcode response object in the API.
        This is not a nice way of doing it, but means we only hit the db once, and can figure out how to do it nicer
        after May 6th.
        """
        gss_codes = {
            a: a.uprntocouncil.lad for a in self.addresses if a.uprntocouncil.lad
        }

        council_map = {
            v[0]: v
            for v in CouncilGeography.objects.filter(
                gss__in=set(gss_codes.values())
            ).values_list("gss", "council_id", "council__name")
        }
        """
        This is a bit of a hack because it adds a property to each address objects in self.addresses, so that
        it is already set when the address serializer populates the 'council' field with the council_name property
        from each address.
        """
        for address, gss in gss_codes.items():
            address._council_name = council_map.get(gss)[2]

        if len(council_map) == 1:
            return None
        return [v[1] for v in council_map.values()]

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
        return False

    @property
    def elections_response(self):
        if not self._elections_response:
            self.lookup_elections()
        return self._elections_response

    def lookup_elections(self):
        self._elections_response = self.elections_backend().get_response(self.postcode)
        return self._elections_response

    @property
    def split_elections(self):
        if self.elections_response.get("address_picker"):
            return True
        return False

    @cached_property
    def route_type(self):
        if not self.has_addresses:
            # Postcode is not in addressbase
            return "postcode"
        if self.councils and self.no_stations:
            # multiple councils and no stations for any address in postcode
            return "multiple_addresses"

        self.lookup_elections()

        if self.split_elections:
            return "multiple_addresses"
        if self.no_stations:
            # We don't have any station information for this address
            return "postcode"
        if self.addresses_have_single_station:
            # all the addresses in this postcode
            # map to one polling station
            return "single_address"
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
        return None

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
