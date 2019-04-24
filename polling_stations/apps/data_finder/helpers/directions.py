import abc
import json
import random
import requests
import urllib
from collections import namedtuple
from django.conf import settings
from django.utils.translation import ugettext as _


Directions = namedtuple(
    "Directions", ["time", "dist", "mode", "route", "precision", "source"]
)


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

        time = str(directions["routes"][0]["legs"][0]["duration"]["text"]).replace(
            "mins", _("minute")
        )

        dist = str(directions["routes"][0]["legs"][0]["distance"]["text"]).replace(
            "mi", _("miles")
        )

        return Directions(
            time,
            dist,
            transport_verb["base"],
            json.dumps(route),
            self.precision,
            "Google",
        )


class MapzenDirectionsClient(DirectionsClient):

    precision = 6

    def get_base_url(self):
        return "{base}?api_key={key}".format(
            base=settings.BASE_MAPZEN_URL, key=settings.MAPZEN_API_KEY
        )

    def get_data(self, url):
        resp = requests.get(url)
        if resp.status_code != 200:
            raise DirectionsException(
                "Mapzen Directions API error: HTTP status code %i" % resp.status_code
            )
        return resp.json()

    def get_api_key(self):
        return settings.MAPZEN_API_KEY

    def get_route(self, start, end):
        if self.get_api_key() == "":
            raise DirectionsException("No Mapzen Directions API key set")

        query = {
            "locations": [
                {"lat": start.y, "lon": start.x},
                {"lat": end.y, "lon": end.x},
            ],
            "costing": "pedestrian",
            "directions_options": {"units": "miles"},
            "id": "polling_station_route",
        }
        url = "{base_url}&json={json}".format(
            base_url=self.get_base_url(),
            json=urllib.parse.quote_plus(json.dumps(query)),
        )

        directions = self.get_data(url)

        if directions["trip"]["status"] != 0:
            raise DirectionsException(
                "Mapzen Directions API error: {}".format(directions["trip"]["status"])
            )

        route = directions["trip"]["legs"][0]["shape"]

        time = str(int(round(directions["trip"]["summary"]["time"] / 60, 0))) + _(
            " minute"
        )

        dist = str(round(directions["trip"]["summary"]["length"], 1)) + _(" miles")

        return Directions(
            time, dist, "walk", json.dumps(route), self.precision, "Mapzen"
        )


class DirectionsHelper:
    def get_directions(self, **kwargs):
        if kwargs["start_location"] and kwargs["end_location"]:
            clients = (GoogleDirectionsClient(),)
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
