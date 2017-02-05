import logging
import lxml.etree
import re
import requests
import time
from collections import namedtuple

from django.utils.translation import ugettext as _
from django.contrib.gis.geos import Point
from django.conf import settings

from addressbase.helpers import centre_from_points_qs
from addressbase.models import Address

from pollingstations.models import ResidentialAddress

class PostcodeError(Exception):
    pass

class RateLimitError(Exception):
    def __init__(self, message):
        logger = logging.getLogger('django.request')
        logger.error(message)


def geocode_point_only(postcode):
    """
    Try to get centre of the point from AddressBase, fall back to MapIt
    """
    addresses = Address.objects.filter(postcode=postcode)
    if not addresses:
        time.sleep(1.3)
        return geocode(postcode)

    centre = centre_from_points_qs(addresses)
    return {
        'wgs84_lon': centre.x,
        'wgs84_lat': centre.y,
    }

def geocode(postcode):
    """
    Use MaPit to convert the postcode to a location and constituency
    """

    COUNCIL_TYPES = [
        "LBO",
        "DIS",
        "MTD",
        "LGD",
        "UTA",
    ]


    headers = {}
    if settings.MAPIT_UA:
        headers['User-Agent'] = settings.MAPIT_UA

    res = requests.get("%s/postcode/%s" % (settings.MAPIT_URL, postcode), headers=headers)

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

    res_json = res.json()

    gss_codes = []
    council_gss = None
    for area in res_json['areas']:
        if 'gss' in res_json['areas'][area]['codes']:
            gss = res_json['areas'][area]['codes']['gss']
            gss_codes.append(gss)
            if res_json['areas'][area]['type'] in COUNCIL_TYPES:
                council_gss = gss

    return {
        'wgs84_lon': res_json['wgs84_lon'],
        'wgs84_lat': res_json['wgs84_lat'],
        'gss_codes': gss_codes,
        'council_gss': council_gss,
    }


class AddressSorter:
    # Class for sorting sort a list of tuples
    # containing addresses (defined by key function)
    # in a human-readable order.

    def convert(self, text):
        # if text is numeric, covert to an int
        # this allows us to sort numbers in int order, not string order
        return int(text) if text.isdigit() else text

    def alphanum_key(self, tup):
        # split the desired component of tup (defined by key function)
        # into a listof numeric and text components
        return [ self.convert(c) for c in filter(None, re.split('([0-9]+)', self.key(tup))) ]

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

    def natural_sort(self, lst, key):
        self.key = key
        return sorted(lst, key = self.swap_fields)


class OrsDirectionsApiError(Exception):
    pass


class GoogleDirectionsApiError(Exception):
    pass


class DirectionsHelper():

    def __init__(self):
        self.re_time = re.compile("PT([0-9]+)M([0-9]+)S")
        self.Directions = namedtuple('Directions', ['walk_time', 'walk_dist', 'route'])

    def get_ors_route(self, longlat_from, longlat_to):
        url = settings.ORS_ROUTE_URL_TEMPLATE.format(longlat_from.x, longlat_from.y, longlat_to.x, longlat_to.y)

        resp = requests.get(url)
        if resp.status_code != 200:
            raise OrsDirectionsApiError("Open Route Service API error: HTTP status code %i" % resp.status_code)

        root = lxml.etree.fromstring(resp.content)

        ns = {
            "xls": "http://www.opengis.net/xls",
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "gml": "http://www.opengis.net/gml",
        }

        ps = [
            [float(x) for x in pos.text.split()]
            for pos in root.xpath('//xls:RouteGeometry/gml:LineString/gml:pos', namespaces=ns)
        ]

        walk_dist = "{} {}".format(
            root.xpath('//xls:RouteSummary/xls:TotalDistance/@value', namespaces=ns)[0],
            _('miles'),
        )

        time_text = root.xpath('//xls:RouteSummary/xls:TotalTime/text()', namespaces=ns)[0]
        matches = self.re_time.match(
            time_text,
        )
        if matches is not None:
            walk_time = "{} {}".format(matches.group(1), _('minute'))
        else:
            walk_time = None

        return self.Directions(walk_time, walk_dist, ps)

    def get_google_route(self, postcode, end):
        url = "{base_url}{postcode}&destination={destination}".format(
                base_url=settings.BASE_GOOGLE_URL,
                postcode=postcode,
                destination="{0},{1}".format(end.y, end.x),
            )

        resp = requests.get(url)
        if resp.status_code != 200:
            raise GoogleDirectionsApiError("Google Directions API error: HTTP status code %i" % resp.status_code)
        directions = resp.json()

        if directions['status'] != 'OK':
            raise GoogleDirectionsApiError("Google Directions API error: {}".format(directions['status']))

        start_points = [
            Point(x['start_location']['lng'], x['start_location']['lat'])
            for x in directions['routes'][0]['legs'][0]['steps']
        ]

        end_points = [
            Point(x['end_location']['lng'], x['end_location']['lat'])
            for x in directions['routes'][0]['legs'][0]['steps']
        ]

        walk_time = str(
            directions['routes'][0]['legs'][0]['duration']['text']
        ).replace('mins', _('minute'))

        walk_dist = str(
            directions['routes'][0]['legs'][0]['distance']['text']
        ).replace('mi', _('miles'))

        return self.Directions(walk_time, walk_dist, start_points[:] + end_points[-1:])

    def get_directions(self, **kwargs):
        try:
            directions = self.get_google_route(kwargs['start_postcode'], kwargs['end_location'])
        except GoogleDirectionsApiError as e1:
            return None
            # Should log error here

            if kwargs['start_location']:
                try:
                    directions = self.get_ors_route(kwargs['start_location'], kwargs['end_location'])
                except OrsDirectionsApiError as e2:
                    # Should log error here

                    directions = None
            else:
                directions = None

        return directions


# use a postcode do decide which endpoint the user should be directed to
class RoutingHelper():

    def __init__(self, postcode):
        self.postcode = postcode.replace(' ', '')
        self.Endpoint = namedtuple('Endpoint', ['view', 'kwargs'])
        self.get_addresses()

    def get_addresses(self):
        self.addresses = ResidentialAddress.objects.filter(
            postcode=self.postcode
        )#.distinct()
        return self.addresses

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
