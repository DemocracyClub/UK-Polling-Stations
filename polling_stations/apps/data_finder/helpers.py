import abc
import logging
import lxml.etree
import re
import requests
import time
from collections import namedtuple
from operator import itemgetter

from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse

from uk_geo_utils.helpers import centre_from_points_qs
from addressbase.models import Address, Blacklist
from uk_geo_utils.models import Onsud

from pollingstations.models import Council, ResidentialAddress
from pollingstations.helpers import format_postcode_no_space, format_postcode_with_space
from data_finder.directions_clients import (
    DirectionsException, GoogleDirectionsClient, MapzenDirectionsClient)


class PostcodeError(Exception):
    pass

class MultipleCouncilsException(Exception):
    pass

class CodesNotFoundException(Exception):
    pass

class RateLimitError(Exception):
    def __init__(self, message):
        logger = logging.getLogger('django.request')
        logger.error(message)


class BaseGeocoder(metaclass=abc.ABCMeta):

    def __init__(self, postcode):
        self.postcode = self.format_postcode(postcode)

    def format_postcode(self, postcode):
        return postcode

    @abc.abstractmethod
    def geocode_point_only(self):
        pass

    @abc.abstractmethod
    def geocode(self):
        pass

    def run(self, point_only=False):
        if point_only:
            return self.geocode_point_only()
        else:
            return self.geocode()


class MapitGeocoder(BaseGeocoder):

    def call_mapit(self):
        headers = {}
        if settings.MAPIT_UA:
            headers['User-Agent'] = settings.MAPIT_UA

        res = requests.get("%s/postcode/%s" % (settings.MAPIT_URL, self.postcode), headers=headers)

        if res.status_code != 200:
            if res.status_code == 403:
                # we hit MapIt's rate limit
                raise RateLimitError("Mapit error 403: Rate limit exceeded")

            if res.status_code == 404:
                # if mapit returns 404, it returns HTML even if we requested json
                # this will cause an unhandled exception if we try to parse it
                raise PostcodeError("Mapit error 404: Not Found")

            try:
                # attempt to parse error from json
                res_json = res.json()
                if 'error' in res_json:
                    raise PostcodeError("Mapit error {}: {}".format(res_json['code'], res_json['error']))
                else:
                    raise PostcodeError("Mapit error {}: unknown".format(res.status_code))
            except ValueError:
                # if we fail to parse json, raise a less specific exception
                raise PostcodeError("Mapit error {}: unknown".format(res.status_code))

        return res.json()

    def geocode(self):
        res_json = self.call_mapit()
        COUNCIL_TYPES = getattr(settings, 'COUNCIL_TYPES', [])
        gss_codes = []
        council_gss = None
        for area in res_json['areas']:
            if 'gss' in res_json['areas'][area]['codes']:
                gss = res_json['areas'][area]['codes']['gss']
                gss_codes.append(gss)
                if res_json['areas'][area]['type'] in COUNCIL_TYPES:
                    council_gss = gss

        if 'wgs84_lon' not in res_json or 'wgs84_lat' not in res_json:
            raise PostcodeError("No location information")

        return {
            'source': 'mapit',
            'wgs84_lon': res_json['wgs84_lon'],
            'wgs84_lat': res_json['wgs84_lat'],
            'gss_codes': gss_codes,
            'council_gss': council_gss,
        }

    def geocode_point_only(self):
        return self.geocode()


class AddressBaseGeocoder(BaseGeocoder):

    def format_postcode(self, postcode):
        # postcodes in AddressBase are in format AA1 1AA
        # ensure postcode is formatted correctly before we try to query
        return format_postcode_with_space(postcode)

    def get_uprns(self, addresses):
        return [a.uprn for a in addresses]

    def get_codes(self, uprns):
        addresses = Onsud.objects.filter(uprn__in=uprns)

        if len(addresses) == 0:
            # No records in the ONSUD table were found for the given UPRNs
            # because...reasons
            raise CodesNotFoundException('Found no records in ONSUD for supplied UPRNs')

        if len(addresses) != len(uprns):
            # For the moment I'm going to do nothing about this, but lets
            # leave this condition here to make that decision explicit
            # TODO: maybe we should actually do....something else??
            pass

        council_ids = set([a.lad for a in addresses])

        # assemble list of codes
        gss_codes = set()
        for address in addresses:
            extra_codes = [address.cty, address.lad, address.ctry, address.rgn, address.eer]
            for code in extra_codes:
                gss_codes.add(code)

        if len(council_ids) == 1:
            # all the uprns supplied are in the same local authority
            council_gss = list(council_ids)[0]
        else:
            # the urpns supplied are in multiple local authorities
            raise MultipleCouncilsException('Postcode %s covers UPRNs in more than one local authority' % (self.postcode))

        return {
            'council_gss': council_gss,
            'gss_codes': list(gss_codes)
        }

    def geocode(self):
        addresses = Address.objects.filter(postcode=self.postcode)
        if not addresses:
            raise ObjectDoesNotExist('No addresses found for postcode %s' % (self.postcode))

        codes = self.get_codes(self.get_uprns(addresses))
        centre = centre_from_points_qs(addresses)
        return {
            'source': 'addressbase',
            'wgs84_lon': centre.x,
            'wgs84_lat': centre.y,
            'council_gss': codes['council_gss'],
            'gss_codes': codes['gss_codes'],
        }

    def geocode_point_only(self):
        addresses = Address.objects.filter(postcode=self.postcode)
        if not addresses:
            raise ObjectDoesNotExist('No addresses found for postcode %s' % (self.postcode))

        centre = centre_from_points_qs(addresses)
        return {
            'source': 'addressbase',
            'wgs84_lon': centre.x,
            'wgs84_lat': centre.y,
        }


def geocode_point_only(postcode, sleep=True):
    geocoders = (AddressBaseGeocoder(postcode), MapitGeocoder(postcode))
    for geocoder in geocoders:
        try:
            return geocoder.run(True)
        except ObjectDoesNotExist:
            # we couldn't find this postcode in AddressBase
            # fall back to the next source

            # optional sleep to avoid hammering external services
            if sleep:
                time.sleep(1.3)

            continue
        except PostcodeError:
            # we were unable to geocode this postcode using mapit
            # re-raise the exception.
            # Note: in future we may want to fall back to yet another source
            raise
        except:
            # something else went wrong:
            # lets give the next source a try anyway

            # optional sleep to avoid hammering external services
            if sleep:
                time.sleep(1.3)

            continue

    # All of our attempts to geocode this failed. Raise a generic exception
    raise PostcodeError('Could not geocode from any source')


def geocode(postcode):
    geocoders = (AddressBaseGeocoder(postcode), MapitGeocoder(postcode))
    for geocoder in geocoders:
        try:
            return geocoder.run(False)
        except ObjectDoesNotExist:
            # we couldn't find this postcode in AddressBase
            # fall back to the next source
            continue
        except CodesNotFoundException:
            # we did find this postcode in AddressBase, but there were no
            # corresponding codes in ONSUD: fall back to the next source
            continue
        except MultipleCouncilsException:
            # this postcode contains uprns in multiple local authorities
            # re-raise the exception.
            raise
        except PostcodeError:
            # we were unable to geocode this postcode using mapit
            # re-raise the exception.
            # Note: in future we may want to fall back to yet another source
            raise
        except:
            # something else went wrong:
            # lets give the next source a try anyway
            continue

    # All of our attempts to geocode this failed. Raise a generic exception
    raise PostcodeError('Could not geocode from any source')


def get_territory(postcode):
    if postcode[:2] == 'BT':
        return 'NI'
    return 'GB'


def get_council(geocode_result):
    if 'council_gss' in geocode_result:
        try:
            return Council.objects.defer("area", "location").get(
                council_id=geocode_result['council_gss'])
        except Council.DoesNotExist:
            pass

    if 'gss_codes' in geocode_result:
        try:
            return Council.objects.defer("area", "location").get(
                council_id__in=geocode_result['gss_codes'])
        except Council.DoesNotExist:
            pass

    location = Point(geocode_result['wgs84_lon'], geocode_result['wgs84_lat'])
    return Council.objects.defer("area", "location").get(area__covers=location)


class AddressSorter:
    # Class for sorting sort a list of address objects
    # in a human-readable order.

    def __init__(self, addresses):
        self.addresses = addresses

    def convert(self, text):
        # if text is numeric, covert to an int
        # this allows us to sort numbers in int order, not string order
        return int(text) if text.isdigit() else text

    def alphanum_key(self, tup):
        # split the desired component of tup (defined by key function)
        # into a listof numeric and text components
        return [ self.convert(c) for c in filter(None, re.split('([0-9]+)', tup[1])) ]

    def swap_fields(self, item):
        lst = self.alphanum_key(item)
        # swap things about so we can sort by street name, house number
        # instead of house number, street name
        if len(lst) > 1 and isinstance(lst[0], int) and isinstance(lst[1], str) and (lst[1][0].isspace() or lst[1][0] == ','):
            lst[0], lst[1] = lst[1], lst[0]
        if len(lst) > 1 and isinstance(lst[0], int) and isinstance(lst[1], int):
            lst[0], lst[1] = lst[1], lst[0]
        if isinstance(lst[0], int):
            lst[0] = str(lst[0])
        return lst

    def natural_sort(self):
        sorted_list = sorted(
            [(address, address.address) for address in self.addresses],
            key=self.swap_fields
        )
        return [address[0] for address in sorted_list]


class EveryElectionWrapper:

    def __init__(self, postcode):
        try:
            self.elections = self.get_data(postcode)
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

        if len(self.elections) > 0:
            return True

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
            clients = (MapzenDirectionsClient(), GoogleDirectionsClient(),)
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
        self.postcode = format_postcode_no_space(postcode)
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
