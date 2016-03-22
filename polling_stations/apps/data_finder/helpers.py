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


Directions = namedtuple('Directions', ['walk_time', 'walk_dist', 'route'])


class OrsDirectionsApiError(Exception):
    pass


re_time = re.compile("PT([0-9]+)M([0-9]+)S")

def get_ors_route(longlat_from, longlat_to):
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
    matches = re_time.match(
        time_text,
    )
    if matches is not None:
        walk_time = "{} {}".format(matches.group(1), _('minute'))
    else:
        walk_time = None

    return Directions(walk_time, walk_dist, ps)


class GoogleDirectionsApiError(Exception):
    pass


def get_google_route(postcode, end):
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

    return Directions(walk_time, walk_dist, start_points[:] + end_points[-1:])

