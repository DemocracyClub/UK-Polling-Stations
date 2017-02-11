import logging
import lxml.etree
import re
import requests
import time
from collections import namedtuple

from django.utils.translation import ugettext as _
from django.contrib.gis.geos import Point
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from addressbase.helpers import centre_from_points_qs
from addressbase.models import Address, Onsad

from pollingstations.models import ResidentialAddress


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


class MapitWrapper:

    def __init__(self, postcode):
        self.postcode = postcode

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

        return {
            'source': 'mapit',
            'wgs84_lon': res_json['wgs84_lon'],
            'wgs84_lat': res_json['wgs84_lat'],
            'gss_codes': gss_codes,
            'council_gss': council_gss,
        }


class AddressBaseWrapper:

    def __init__(self, postcode):
        self.postcode = self.format_postcode(postcode)

    def format_postcode(self, postcode):
        # postcodes in AddressBase are in format AA1 1AA
        # ensure postcode is formatted correctly before we try to query
        postcode = re.sub('[^A-Z0-9]', '', postcode.upper())
        postcode = postcode[:-3] + ' ' + postcode[-3:]
        return postcode

    def get_uprns(self, addresses):
        return [a.uprn for a in addresses]

    def get_codes(self, uprns):
        addresses = Onsad.objects.filter(uprn__in=uprns)

        if len(addresses) == 0:
            # No records in the ONSAD table were found for the given UPRNs
            # because...reasons
            raise CodesNotFoundException('Found no records in ONSAD for supplied UPRNs')

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
    addressbase = AddressBaseWrapper(postcode)
    mapit = MapitWrapper(postcode)

    try:
        # first try addressbase
        result = addressbase.geocode_point_only()
    except ObjectDoesNotExist:
        # we couldn't find this postcode in AddressBase: fall back to mapit

        # optional sleep to avoid hammering mapit
        if sleep:
            time.sleep(1.3)

        result = mapit.geocode()
    except:
        # something else went wrong: lets give mapit a go anyway

        # optional sleep to avoid hammering mapit
        if sleep:
            time.sleep(1.3)

        result = mapit.geocode()

    return result


def geocode(postcode):
    addressbase = AddressBaseWrapper(postcode)
    mapit = MapitWrapper(postcode)

    try:
        # first try addressbase
        result = addressbase.geocode()
    except ObjectDoesNotExist:
        # we couldn't find this postcode in AddressBase: fall back to mapit
        result = mapit.geocode()
    except CodesNotFoundException:
        # we did find this postcode in AddressBase, but there were no
        # corresponding codes in ONSAD: fall back to mapit
        result = mapit.geocode()
    except MultipleCouncilsException:
        # this postcode contains uprns in multiple local authorities
        # re-raise the exception.
        raise
    except:
        # something else went wrong: lets give mapit a go anyway
        result = mapit.geocode()

    return result


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
