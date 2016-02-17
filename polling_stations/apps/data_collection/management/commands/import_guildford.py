"""
Imports Guildford
"""
from django.contrib.gis.geos import Point, GEOSGeometry

from data_collection.management.commands import BaseKamlImporter
from data_collection.google_geocoding_api_wrapper import (
    GoogleGeocodingApiWrapper,
    PostcodeNotFoundException
)


class Command(BaseKamlImporter):
    """
    Imports the Polling Station data from Guildford Council
    """
    council_id     = 'E07000209'
    # KML file originally supplied was malformed
    # so we work with a version that has been repaired so it will parse properly
    districts_name = 'GuildfordBoroughCouncilPollingDistricts20150325-fixed.kml'
    stations_name  = 'GuildfordBoroughCouncilPollingPlaces20150325.csv'

    def district_record_to_dict(self, record):
        # this kml has no altitude co-ordinates so the data is ok as it stands
        geojson = record.geom.geojson

        # The SRID for the KML is 4326 but the CSV is 2770 so we
        # set it each time we create the polygon.
        # We could probably do with a more elegant way of doing
        # this longer term.
        self._srid = self.srid
        self.srid = 4326
        poly = self.clean_poly(GEOSGeometry(geojson, srid=self.srid))
        self.srid = self._srid

        return {
            'internal_council_id': record['register'].value,
            'extra_id'           : record['mi_prinx'].value,
            'name'               : record['pollingdistrictname'].value,
            'area'               : poly
        }

    def station_record_to_dict(self, record):
        location = Point(float(record.easting), float(record.northing), srid=self.srid)

        # assemble address and extract postcode if present
        thoroughfare_parts = record.thoroughfare_name.strip().split(', ')
        address_tail = thoroughfare_parts[-1]
        if len(address_tail) >= 6 and len(address_tail) <= 8 and ' ' in address_tail and address_tail != 'Ash Vale':
            address = "\n".join(record.pollingplace.strip().split(', ') + thoroughfare_parts[:-1])
            postcode = address_tail
        else:
            address = "\n".join(record.pollingplace.strip().split(', ') + thoroughfare_parts)

            # attempt to attach postcode if missing
            gwrapper = GoogleGeocodingApiWrapper(address + ', Guildford, UK')
            try:
                postcode = gwrapper.address_to_postcode()
            except PostcodeNotFoundException:
                postcode = ''

        return {
            'internal_council_id': record.register.strip(),
            'postcode':            postcode,
            'address':             address,
            'location':            location
        }
