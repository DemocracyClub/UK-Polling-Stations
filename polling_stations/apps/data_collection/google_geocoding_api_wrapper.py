import urllib.parse, urllib.request
import json
from time import sleep


"""
Custom exception thrown if no matching postcode found
"""
class PostcodeNotFoundException(Exception):
    pass


"""
Wrapper class for Google Maps Geocoding API
"""
class GoogleGeocodingApiWrapper:

    def __init__(self, address):
        self.address = address

    def geocode(self):
        sleep(0.2)  # ensure we don't hit QUERY_LIMIT
        address = urllib.parse.quote(self.address)
        url = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address=%s' % address
        req = urllib.request.urlopen(url)
        str_response = req.read().decode('utf-8')
        json_response = json.loads(str_response)
        return json_response

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
                        return component['long_name']
        raise PostcodeNotFoundException("No postcode found")
