import requests
import re
import lxml.etree
from collections import namedtuple

from django.utils.translation import ugettext as _
from django.contrib.gis.geos import Point

from data_collection import constants


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

        directions = requests.get(url).json()

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

            try:
                directions = self.get_ors_route(kwargs['start_location'], kwargs['end_location'])
            except OrsDirectionsApiError as e2:
                # Should log error here

                directions = None

        return directions
