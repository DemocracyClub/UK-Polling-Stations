import urllib.parse, urllib.request, requests
import json
from time import sleep
from data_collection import constants


"""
Custom exception thrown if no matching postcode found
"""
class PostcodeNotFoundException(Exception):
    pass


"""
Wrapper class for Google Maps Geocoding API
"""
class GoogleGeocodingApiWrapper:

    def __init__(self, address, area_code=None, area_type=None):
        self.address = address
        self.area_code = area_code
        self.area_type = area_type

    def geocode(self):
        sleep(0.2)  # ensure we don't hit QUERY_LIMIT
        address = urllib.parse.quote(self.address)
        url = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address=%s' % address
        req = urllib.request.urlopen(url)
        str_response = req.read().decode('utf-8')
        json_response = json.loads(str_response)
        return json_response

    """
    If self.area_code is set, use mapit to check that
    the postcode we've found is in the area
    (probably local auth, but if we have ward or something, use that)
    that it is supposed to be in
    Otherwise raises exception of class PostcodeNotFoundException
    """
    def sanity_check(self, postcode):
        sleep(1)  # ensure we don't hit mapit's usage limit
        res = requests.get("%s/postcode/%s" % (constants.MAPIT_URL, postcode))
        res_json = res.json()

        for area in res_json['areas']:
            if res_json['areas'][area]['type'] == self.area_type:
                if res_json['areas'][area]['codes']['gss'] != self.area_code:
                    raise PostcodeNotFoundException("Postcode found but sanity check failed")
        return True

    """
    Returns postcode if we have a decent match
    Otherwise raises exception of class PostcodeNotFoundException
    """
    def address_to_postcode(self):
        response = self.geocode()
        if response['status'] == 'OK':
            for result in response['results']:
                for component in result['address_components']:
                    if 'postal_code' in component['types'] and len(component['long_name']) >= 5:
                        if self.area_code is not None and self.area_type is not None:
                            self.sanity_check(component['long_name'])
                        return component['long_name']
        raise PostcodeNotFoundException("No postcode found")
