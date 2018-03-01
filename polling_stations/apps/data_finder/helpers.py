import abc
import logging
import re
import requests
from collections import namedtuple
from operator import itemgetter

from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse

from addressbase.models import Address, Blacklist
from uk_geo_utils.helpers import Postcode
from uk_geo_utils.geocoders import (
    AddressBaseGeocoder,
    OnspdGeocoder,
    AddressBaseException,
    MultipleCodesException
)

from pollingstations.models import Council, ResidentialAddress
from data_finder.directions_clients import (
    DirectionsException, GoogleDirectionsClient, MapzenDirectionsClient)


class PostcodeError(Exception):
    pass

class MultipleCouncilsException(MultipleCodesException):
    pass


class BaseGeocoder(metaclass=abc.ABCMeta):

    def __init__(self, postcode):
        self.postcode = self.format_postcode(postcode)

    def format_postcode(self, postcode):
        return Postcode(postcode).without_space

    @abc.abstractmethod
    def geocode_point_only(self):
        pass

    @abc.abstractmethod
    def geocode(self):
        pass


class OnspdGeocoderAdapter(BaseGeocoder):

    def geocode(self):
        geocoder = OnspdGeocoder(self.postcode)
        centre = geocoder.centroid
        if not centre:
            raise PostcodeError("No location information")

        local_auth = geocoder.get_code('lad')
        error_values = [
            'L99999999', # Channel Islands
            'M99999999', # Isle of Man
            '' # Terminated Postcode or other
        ]
        if not local_auth or local_auth in error_values:
            raise PostcodeError("No location information")

        return geocoder

    def geocode_point_only(self):
        geocoder = OnspdGeocoder(self.postcode)
        centre = geocoder.centroid
        if not centre:
            raise PostcodeError("No location information")
        return geocoder


class AddressBaseGeocoderAdapter(BaseGeocoder):

    def geocode(self):
        geocoder = AddressBaseGeocoder(self.postcode)
        centre = geocoder.centroid

        try:
            lad = geocoder.get_code('lad')
        except MultipleCodesException as e:
            # re-raise as a more specific MultipleCouncilsException
            # because that is what the calling code expects to handle
            raise MultipleCouncilsException(str(e))

        return geocoder

    def geocode_point_only(self):
        return AddressBaseGeocoder(self.postcode)


def geocode_point_only(postcode):
    geocoders = (AddressBaseGeocoderAdapter(postcode), OnspdGeocoderAdapter(postcode))
    for geocoder in geocoders:
        try:
            return geocoder.geocode_point_only()
        except ObjectDoesNotExist:
            # we couldn't find this postcode in AddressBase
            # this might be because
            # - The postcode isn't in AddressBase
            # - The postcode is in Northern Ireland
            # - AddressBase hasn;t been imported
            # fall back to the next source
            continue
        except PostcodeError:
            # we were unable to geocode this postcode using ONSPD
            # re-raise the exception.
            # Note: in future we may want to fall back to yet another source
            raise

    # All of our attempts to geocode this failed. Raise a generic exception
    raise PostcodeError('Could not geocode from any source')


def geocode(postcode):
    geocoders = (AddressBaseGeocoderAdapter(postcode), OnspdGeocoderAdapter(postcode))
    for geocoder in geocoders:
        try:
            return geocoder.geocode()
        except ObjectDoesNotExist:
            # we couldn't find this postcode in AddressBase
            # this might be because
            # - The postcode isn't in AddressBase
            # - The postcode is in Northern Ireland
            # - AddressBase hasn;t been imported
            # fall back to the next source
            continue
        except MultipleCouncilsException:
            # this postcode contains uprns in multiple local authorities
            # re-raise the exception.
            raise
        except AddressBaseException:
            # we did find this postcode in AddressBase, but there were no
            # corresponding codes in ONSUD: fall back to the next source
            continue
        except PostcodeError:
            # we were unable to geocode this postcode using ONSPD
            # re-raise the exception.
            # Note: in future we may want to fall back to yet another source
            raise

    # All of our attempts to geocode this failed. Raise a generic exception
    raise PostcodeError('Could not geocode from any source')


def get_council(geocode_result):
    try:
        return Council.objects.defer("area").get(
            council_id=geocode_result.get_code('lad'))
    except Council.DoesNotExist:
        return Council.objects.defer("area").get(
            area__covers=geocode_result.centroid)


class EveryElectionWrapper:

    def __init__(self, postcode):
        try:
            self.elections = self.get_data(Postcode(postcode).with_space)
            self.request_success = True
        except:
            self.request_success = False

    def get_data(self, postcode):
        headers = {}
        if hasattr(settings, 'CUSTOM_UA'):
            headers['User-Agent'] = settings.CUSTOM_UA

        res = requests.get("%sapi/elections.json?postcode=%s&future=1" % (
            settings.EE_BASE, postcode), timeout=4, headers=headers)

        if res.status_code != 200:
            res.raise_for_status()

        res_json = res.json()
        return res_json['results']

    def has_election(self):
        if not self.request_success:
            # if the request was unsucessful for some reason,
            # assume there *is* an upcoming election
            return True

        ballots = filter(lambda e: e['group_type'] is None, self.elections)
        try:
            next(ballots)
            return True
        except StopIteration:
            return False

    def get_explanations(self):
        explanations = []
        if not self.request_success:
            # if the request was unsucessful for some reason,
            # return no explanations
            return explanations

        if len(self.elections) > 0:
            for election in self.elections:
                if 'explanation' in election and election['explanation']:
                    explanations.append({
                        'title': election['election_title'],
                        'explanation': election['explanation'],
                    })
        return explanations


class DirectionsHelper():

    def get_directions(self, **kwargs):
        if kwargs['start_location'] and kwargs['end_location']:
            clients = (GoogleDirectionsClient(),)
            for client in clients:
                try:
                    return client.get_route(kwargs['start_location'], kwargs['end_location'])
                except DirectionsException:
                    pass
            return None
        else:
            return None


# use a postcode to decide which endpoint the user should be directed to
class RoutingHelper():

    def __init__(self, postcode):
        self.postcode = Postcode(postcode).without_space
        self.Endpoint = namedtuple('Endpoint', ['view', 'kwargs'])
        self.get_addresses()
        self.get_councils_from_blacklist()

    def get_addresses(self):
        self.addresses = ResidentialAddress.objects.filter(
            postcode=self.postcode
        )#.distinct()
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
        if getattr(self, 'addresses', None):
            self.get_addresses()
        return bool(self.addresses)

    @property
    def has_single_address(self):
        if getattr(self, 'addresses', None):
            self.get_addresses()
        return self.addresses.count == 1

    @property
    def address_have_single_station(self):
        if getattr(self, 'addresses', None):
            self.get_addresses()
        stations = self.addresses.values('polling_station_id').distinct()
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


    def get_endpoint(self):
        if self.route_type == "multiple_councils":
            # this postcode contains UPRNS situated in >1 local auth
            # maybe one day we will handle this better, but for now
            # we just throw a special "we don't know" page
            # ..even if we might possibly know
            return self.Endpoint(
                'multiple_councils_view',
                {'postcode': self.postcode}
            )
        if self.route_type == "single_address":
            # all the addresses in this postcode
            # map to one polling station
            return self.Endpoint(
                'address_view',
                {'address_slug': self.addresses[0].slug}
            )
        if self.route_type == "multiple_addresses":
            # addresses in this postcode map to
            # multiple polling stations
            return self.Endpoint(
                'address_select_view',
                {'postcode': self.postcode}
            )
        if self.route_type == "postcode":
            # postcode is not in ResidentialAddress table
            return self.Endpoint(
                'postcode_view',
                {'postcode': self.postcode}
            )
