from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseCsvStationsShpDistrictsImporter

"""
Ashfield publish their data on data.gov.uk :D
..but they publish Excel and MapInfo binaries :(

I've converted these to CSV and SHP format
and uploaded that data to Amazon S3 for import purposes

Additionally there's a hashes only scraper at
https://morph.io/wdiv-scrapers/DC-PollingStations-Ashfield
polling the URLs to look for changes.
"""

class Command(BaseCsvStationsShpDistrictsImporter):
    council_id = 'E07000170'
    srid = 4326
    districts_srid = 27700
    districts_name = 'polling_districts_2016-12-18'
    stations_name = 'polling_stations_2016-12-18.csv'
    csv_delimiter = ','
    elections = ['local.nottinghamshire.2017-05-04']

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': str(record[0]).strip(),
            'name': '%s - %s' % (str(record[1]).strip(), str(record[0]).strip()),
            'polling_station_id': str(record[3]).strip(),
        }

    def station_record_to_dict(self, record):
        location = Point(float(record.x), float(record.y), srid=self.srid)
        return {
            'internal_council_id': record.id,
            'address' : '%s\n%s' % (record.name, record.address),
            'postcode': '',
            'location': location,
        }
