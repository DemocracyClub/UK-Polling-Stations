"""
Imports Plymouth
"""
from django.contrib.gis.geos import Point, GEOSGeometry

from data_collection.management.commands import BaseKamlImporter
from data_collection.google_geocoding_api_wrapper import (
    GoogleGeocodingApiWrapper,
    PostcodeNotFoundException
)


class Command(BaseKamlImporter):
    """
    Imports the Polling Station data from Plymouth Council
    """
    council_id     = 'E06000026'
    districts_name = 'Plymouth_Polling_Districts.kml'
    stations_name  = 'Plymouth Polling Stations.csv'

    def district_record_to_dict(self, record):
        # this kml has no altitude co-ordinates so the data is ok as it stands
        geojson = record.geom.geojson

        poly = self.clean_poly(GEOSGeometry(geojson, srid=self.get_srid('districts')))

        # manually deal with dodgy/missing data
        if record['DISTRICT'].value == '' and record['NOTES1'].value == 'EGGBUCKLAND' and record['AREA'].value == 689766:
            id = 'HD'
        elif record['DISTRICT'].value == '' and record['NOTES1'].value == 'EGGBUCKLAND' and record['AREA'].value == 594904:
            id = 'HF'
        elif record['DISTRICT'].value == '' and record['NOTES1'].value == '':
            # Drake's Island ( https://en.wikipedia.org/wiki/Drake's_Island )
            # seems to have a polling district but no associated station so can't work out the code.
            # We'll just give it a name:
            id = "Drake's Island"
        else:
            id = record['DISTRICT'].value

        return {
            'internal_council_id': id,
            'name'               : id,
            'area'               : poly
        }

    def station_record_to_dict(self, record):
        location = Point(float(record.east), float(record.north), srid=self.get_srid())

        address = "\n".join([record.addressl1, record.addressl2, record.addressl3])
        if address[-1:] == '\n':
            address = address[:-1]

        # attempt to attach postcodes
        gwrapper = GoogleGeocodingApiWrapper(address + ", Plymouth, UK")
        try:
            postcode = gwrapper.address_to_postcode()
        except PostcodeNotFoundException:
            postcode = ''

        return {
            'internal_council_id': record.statno,
            'postcode':            postcode,
            'address':             address,
            'location':            location
        }
