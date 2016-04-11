import requests
import re
import lxml.etree
from collections import namedtuple

from django.utils.translation import ugettext as _
from django.contrib.gis.geos import Point

from data_collection import constants

from pollingstations.models import ResidentialAddress


class PostcodeError(Exception):
    pass


def geocode(postcode):
    """
    Use MaPit to convert the postcode to a location and constituency
    """
    res = requests.get("%s/postcode/%s" % (constants.MAPIT_URL, postcode))
    res_json = res.json()

    if 'error' in res_json:
        raise PostcodeError("Mapit error {}: {}".format(res_json['code'], res_json['error']))
    else:
        return {
            'wgs84_lon': res_json['wgs84_lon'],
            'wgs84_lat': res_json['wgs84_lat'],
        }


# sort a list of tuples by key in natural/human order
def natural_sort(l, key):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda item: [ convert(c) for c in re.split('([0-9]+)', key(item)) ]
    return sorted(l, key = alphanum_key)


class OrsDirectionsApiError(Exception):
    pass


class GoogleDirectionsApiError(Exception):
    pass


class DirectionsHelper():

    def __init__(self):
        self.re_time = re.compile("PT([0-9]+)M([0-9]+)S")
        self.Directions = namedtuple('Directions', ['walk_time', 'walk_dist', 'route'])

    def get_ors_route(self, longlat_from, longlat_to):
        url = constants.ORS_ROUTE_URL_TEMPLATE.format(longlat_from.x, longlat_from.y, longlat_to.x, longlat_to.y)

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
                base_url=constants.BASE_GOOGLE_URL,
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
