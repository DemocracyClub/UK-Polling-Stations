import abc
import json
import math
import random
from typing import NamedTuple

import requests
from django.conf import settings
from django.contrib.gis.geos import Point


class Directions(NamedTuple):
    time: float  # travel time in seconds
    distance: float  # distance in metres
    mode: str  # mode of transport, either "walk" or "drive"
    route: str  # an encoded polyline (https://developers.google.com/maps/documentation/utilities/polylinealgorithm)
    precision: int  # passed to Leaflet
    source: str  # the directions provider, e.g. "Google" or "MapBox"
    start: Point  # start point
    end: Point  # end point

    @property
    def distance_in_miles(self):
        return self.distance / 1609.34

    @property
    def time_in_minutes(self):
        return math.ceil(self.time / 60)

    # These two URLs have WGS84 coordinates to four decimal places, using
    # https://xkcd.com/2170/ as a guide.

    @property
    def google_maps_url(self):
        return f"https://www.google.com/maps/dir/{self.start.y:.4f},{self.start.x:.4f}/{self.end.y:.4f},{self.end.x:.4f}"

    @property
    def cyclestreets_url(self):
        return f"https://www.cyclestreets.net/journey/{self.start.y:.4f},{self.start.x:.4f}/{self.end.y:.4f},{self.end.x:.4f}/"


def get_google_directions_token():
    keys = settings.GOOGLE_API_KEYS
    if len(keys) == 0:
        return ""
    return random.choice(keys)


def get_distance(start, end):
    # convert the points to British National Grid first
    # so that .distance() will give us a distance in meters
    start_bng = start.transform(27700, clone=True)
    end_bng = end.transform(27700, clone=True)

    distance_km = start_bng.distance(end_bng) / 1000
    return distance_km


class DirectionsException(Exception):
    pass


class DirectionsClient(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_route(self, start, end):
        pass


class GoogleDirectionsClient(DirectionsClient):

    precision = 5

    def get_base_url(self):
        return "{base}&key={key}".format(
            base=settings.BASE_GOOGLE_URL, key=get_google_directions_token()
        )

    def get_data(self, url):
        resp = requests.get(url)
        if resp.status_code != 200:
            raise DirectionsException(
                "Google Directions API error: HTTP status code %i" % resp.status_code
            )
        return resp.json()

    def get_route(self, start, end):
        distance_km = get_distance(start, end)
        if distance_km > 1.5:
            transport_verb = {"base": "drive", "gerund": "driving"}
        else:
            transport_verb = {"base": "walk", "gerund": "walking"}

        url = "{base_url}&mode={mode}&origin={origin}&destination={destination}".format(
            base_url=self.get_base_url(),
            mode=transport_verb["gerund"],
            origin="{0},{1}".format(start.y, start.x),
            destination="{0},{1}".format(end.y, end.x),
        )

        directions = self.get_data(url)

        if directions["status"] != "OK":
            raise DirectionsException(
                "Google Directions API error: {}".format(directions["status"])
            )

        route = directions["routes"][0]["overview_polyline"]["points"]

        return Directions(
            directions["routes"][0]["legs"][0]["duration"]["value"],
            directions["routes"][0]["legs"][0]["distance"]["value"],
            transport_verb["base"],
            json.dumps(route),
            self.precision,
            "Google",
            start,
            end,
        )


class MapboxDirectionsClient(DirectionsClient):
    precision = 5

    def get_data(self, url):
        resp = requests.get(url)
        if resp.status_code != 200:
            raise DirectionsException(
                "Mapbox Directions API error: HTTP status code %i" % resp.status_code
            )
        return resp.json()

    def get_route(self, start, end):
        distance_km = get_distance(start, end)
        if distance_km > 1.5:
            transport_verb = {"base": "drive", "gerund": "driving-traffic"}
        else:
            transport_verb = {"base": "walk", "gerund": "walking"}

        url = "{base_url}/{profile}/{coordinates}?&alternatives=false&geometries=polyline&steps=false&access_token={key}".format(
            base_url=settings.BASE_MAPBOX_URL,
            profile=transport_verb["gerund"],
            coordinates="{start_lon},{start_lat};{end_lon},{end_lat}".format(
                start_lon=start.x, start_lat=start.y, end_lon=end.x, end_lat=end.y
            ),
            key=settings.MAPBOX_API_KEY,
        )

        directions = self.get_data(url)

        if directions["code"] != "Ok":
            raise DirectionsException(
                "Mapbox Directions API error: {}".format(directions["code"])
            )

        return Directions(
            directions["routes"][0]["duration"],
            directions["routes"][0]["distance"],
            transport_verb["base"],
            json.dumps(directions["routes"][0]["geometry"]),
            self.precision,
            "Mapbox",
            start,
            end,
        )


class DirectionsHelper:
    def get_directions(self, **kwargs):
        if kwargs["start_location"] and kwargs["end_location"]:

            clients = (
                MapboxDirectionsClient(),
                GoogleDirectionsClient(),
            )
            for client in clients:
                try:

                    return client.get_route(
                        kwargs["start_location"], kwargs["end_location"]
                    )
                except DirectionsException:
                    pass
            return None
        else:
            return None
