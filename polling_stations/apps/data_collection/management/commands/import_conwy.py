"""
Import Conwy
"""
from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseCsvStationsShpDistrictsImporter

class Command(BaseCsvStationsShpDistrictsImporter):
    """
    Imports the Polling Station data from Conwy Council
    """
    council_id     = 'W06000003'
    districts_name = 'Conwy CBC Polling Districts 20160407'
    stations_name  = 'Conwy CBC Polling Stations (with UPRN) 20160407.csv'
    elections      = [
        'local.conwy.2017-05-04',
        'parl.2017-06-08'
    ]
    ja_count = 0

    def district_record_to_dict(self, record):
        """
        There are 2 different boundaries with code 'JA' but both map to the
        same polling station. Clearly one of them is supposed to be 'JB',
        but we don't know which one so we will import both boundaries and
        assign them our own code to avoid confusion.
        """
        if record[5] == 'JA':
            self.ja_count +=1
            return {
                'internal_council_id': "-".join([record[5], str(self.ja_count)]),
                'name': record[4],
                'polling_station_id': record[5]
            }
        else:
            return {
                'internal_council_id': record[5],
                'name': record[4],
            }

    def station_record_to_dict(self, record):
        try:
            location = Point(int(record.easting), int(record.northing), srid=self.get_srid())
        except ValueError:
            location = Point(float(record.easting), float(record.northing), srid=self.get_srid())

        postcode = record.polling_station_address.split(', ')[-1]
        address = "\n".join(record.polling_station_address.split(', ')[:-1])

        if record.districts == 'JA' or record.districts == 'JB':
            district_id = ''
        else:
            district_id = record.districts

        return {
            'internal_council_id': record.districts,
            'postcode'           : postcode,
            'address'            : address,
            'polling_district_id': district_id,
            'location'           : location
        }
