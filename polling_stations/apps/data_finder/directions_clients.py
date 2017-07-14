import abc
import json
import requests
import urllib
from collections import namedtuple
from django.conf import settings
from django.utils.translation import ugettext as _


Directions = namedtuple('Directions', ['walk_time', 'walk_dist', 'route', 'precision'])


class DirectionsException(Exception):
    pass


class DirectionsClient(metaclass=abc.ABCMeta):

    def __init__(self):
        pass

    @abc.abstractmethod
    def get_route(self, start, end):
        pass


class GoogleDirectionsClient(DirectionsClient):

    precision = 5

    def get_base_url(self):
        return "{base}&key={key}".format(
            base=settings.BASE_GOOGLE_URL,
            key=settings.GOOGLE_API_KEY
        )

    def get_data(self, url):
        resp = requests.get(url)
        if resp.status_code != 200:
            raise DirectionsException("Google Directions API error: HTTP status code %i" % resp.status_code)
        return resp.json()

    def get_route(self, start, end):
        url = "{base_url}&origin={origin}&destination={destination}".format(
                base_url=self.get_base_url(),
                origin="{0},{1}".format(start.y, start.x),
                destination="{0},{1}".format(end.y, end.x),
            )

        directions = self.get_data(url)

        if directions['status'] != 'OK':
            raise DirectionsException("Google Directions API error: {}".format(directions['status']))

        route = directions['routes'][0]['overview_polyline']['points']

        walk_time = str(
            directions['routes'][0]['legs'][0]['duration']['text']
        ).replace('mins', _('minute'))

        walk_dist = str(
            directions['routes'][0]['legs'][0]['distance']['text']
        ).replace('mi', _('miles'))

        return Directions(walk_time, walk_dist, json.dumps(route), self.precision)


class MapzenDirectionsClient(DirectionsClient):

    precision = 6

    def get_base_url(self):
        return "{base}?api_key={key}".format(
            base=settings.BASE_MAPZEN_URL,
            key=settings.MAPZEN_API_KEY
        )

    def get_data(self, url):
        resp = requests.get(url)
        if resp.status_code != 200:
            raise DirectionsException("Mapzen Directions API error: HTTP status code %i" % resp.status_code)
        return resp.json()

    def get_route(self, start, end):
        if settings.MAPZEN_API_KEY == '':
            raise DirectionsException("No Mapzen Directions API key set")

        query = {
            'locations': [
                {
                    'lat': start.y,
                    'lon': start.x,
                },
                {
                    'lat': end.y,
                    'lon': end.x,
                },
            ],
            'costing': 'pedestrian',
            'directions_options': { 'units': 'miles' },
            'id': 'polling_station_route',
        }
        url = "{base_url}&json={json}".format(
            base_url=self.get_base_url(),
            json=urllib.parse.quote_plus(json.dumps(query))
        )

        directions = self.get_data(url)

        if directions['trip']['status'] != 0:
            raise DirectionsException("Mapzen Directions API error: {}".format(directions['trip']['status']))

        route = directions['trip']['legs'][0]['shape']

        walk_time = str(
            int(round(directions['trip']['summary']['time']/60, 0))
        ) + _(" minute")

        walk_dist = str(
            round(directions['trip']['summary']['length'],1)
        ) + _(" miles")

        return Directions(walk_time, walk_dist, json.dumps(route), self.precision)
