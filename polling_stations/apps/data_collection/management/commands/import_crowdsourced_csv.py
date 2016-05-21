"""
Import crowd sourced polling
station data from CSV file or URL

example usage:
./manage.py import_crowdsourced_csv X01000001 -f data/crowdsourcing/ref.2016-06-23/X01000001.csv
./manage.py import_crowdsourced_csv X01000001 -f data/crowdsourcing/pilot/X01000001.csv -c 'latin-1'
./manage.py import_crowdsourced_csv X01000001 -u 'https://docs.google.com/spreadsheet/ccc?key=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&output=csv'
"""

import os
from time import sleep
from django.contrib.gis.geos import Point
from councils.models import Council
from data_collection.management.commands import StationsOnlyCsvImporter
from data_finder.helpers import geocode, PostcodeError
from pollingstations.models import PollingStation

class Command(StationsOnlyCsvImporter):

    def station_record_to_dict(self, record):

        postcode = record.postcode.strip()
        address = record.address.strip()

        if not address and not postcode:
            return None

        # if we have a postcode, attempt to attach a grid ref
        # so we can show the user a map and provide directions
        if postcode:
            sleep(1.3) # ensure we don't hit mapit's usage limit
            try:
                gridref = geocode(postcode)
                location = Point(gridref['wgs84_lon'], gridref['wgs84_lat'], srid=4326)
            except PostcodeError:
                location = None
        else:
            location = None

        return {
            'internal_council_id': record.polling_district_id.strip(),
            'postcode'           : postcode,
            'address'            : address,
            'polling_district_id': record.polling_district_id.strip(),
            'location'           : location
        }
