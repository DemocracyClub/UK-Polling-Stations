import requests
import time

from django.contrib.gis.geos import Point
from lxml import etree

from data_collection.management.commands import BaseMorphApiImporter


class Command(BaseMorphApiImporter):

    srid = 4326
    districts_srid  = 4326
    council_id = 'E07000108'
    elections = ['local.kent.2017-05-04']
    scraper_name = 'wdiv-scrapers/DC-PollingStations-Dover'
    geom_type = 'geojson'

    @property
    def districts_url(self):
        return "%s%s%s&key=%s" % (
            self.base_url, self.scraper_name, self.stations_query, self.morph_api_key)

    def district_record_to_dict(self, record):
        poly = self.extract_geometry(record, self.geom_type, self.get_srid('districts'))
        return {
            'internal_council_id': record['code'],
            'name'               : record['district'],
            'area'               : poly,
            'polling_station_id' : record['code'],
        }

    def station_record_to_dict(self, record):
        gmaps_url = self.extract_link(record['GOOGLE_MAP'])
        location = self.scrape_point_from_gmaps(gmaps_url)
        return {
            'internal_council_id': record['code'],
            'postcode':            '',
            'address':             record['address'],
            'location':            location,
        }

    def extract_link(self, html):
        tree = etree.XML('<div>' + html + '</div>')
        return tree[0][0].attrib['href']

    def scrape_point_from_gmaps(self, url):
        """
        The GeoJSON we harvest from Dover doesn't explicitly contain a grid
        reference for the polling station location. It contains only a
        shortened google maps link (e.g: https://goo.gl/maps/o4fN5T3mFtr )
        To extract a point, we must follow the link and scrape it.
        """
        req = requests.get(url)

        """
        The easiest place to grab the grid reference from is the URL.
        The shortened URL will redirect us to a longer URL like
        https://www.google.co.uk/maps/place/51%C2%B012'48.8%22N+1%C2%B024'08.9%22E/@51.2135538,1.3849626,14z/data=!3m1!4b1!4m5!3m4!1s0x0:0x0!8m2!3d51.21355!4d1.402468
        The bit we want is .../@51.2135538,1.3849626,...
        so we will look for the first @ character and then the next 2 commas
        """
        at = req.url.find('@')
        comma1 = req.url.find(',', at)
        comma2 = req.url.find(',', comma1+1)
        gridref = req.url[at+1:comma2]
        lat, lng = gridref.split(',')
        location = Point(float(lng), float(lat), srid=self.get_srid('stations'))

        # small sleep, just so we don't issue too many requests too quickly
        time.sleep(1.3)

        return location
