from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E09000012'
    addresses_name = 'local.2018-05-03/Version 2/Democracy_Club__03May2018 (1) Hackney.CSV'
    stations_name = 'local.2018-05-03/Version 2/Democracy_Club__03May2018 (1) Hackney.CSV'
    elections = ['local.2018-05-03']

    def station_record_to_dict(self, record):

        if record.polling_place_id == '3082':
            record = record._replace(polling_place_postcode='N1 6EL')

        if record.polling_place_id == '3154':
            rec = super().station_record_to_dict(record)
            rec['location'] = Point(-0.0542398, 51.5677442, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        bad_postcodes = [
            'N1 7GH',
            'E8 3RL',
            'N16 5DG',
            'N16 7DT',
            'E9 7HH',
            'E9 5EE',
            'E1 6JE',
            'N1 7QE',
            'EC2A 4JH',
            'N1 5SB',
            'N4 1SN',
            'E8 1AY',
            'N1 6JB',
            'E5 0QR',
            'N16 9AT',
            'N16 8DJ',
            'E8 2PB',
            'E2 8DP',
            'E2 8FJ',
            'E8 2NS',
            'E8 3BJ',
            'E8 2DP',
            'E5 8NF',
            'N16 6UA',
            'E5 9EG',
            'E5 8HL',
            'E8 2BS',
            'N16 6NA',
            'N16 5TU',
            'E8 4JR',
            'N1 6HD',
            'E5 0AU',
            'E5 0NP',
            'N16 8BX',
            'E5 9AT',
            'EC2A 2ER',
            'E8 1HE',
        ]
        if record.addressline6 in bad_postcodes:
            return None



        if record.addressline6 == 'E5 9ND':
            return None

        rec = super().address_record_to_dict(record)

        if rec and 'coster avenue' in rec['address'].lower():
            return None

        return rec
