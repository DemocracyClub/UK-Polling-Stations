from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E09000023'
    addresses_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018. LEWISHAM.TSV'
    stations_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018. LEWISHAM.TSV'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'

    def address_record_to_dict(self, record):

        uprn = record.property_urn.strip().lstrip('0')

        if uprn == '10070773494':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'SE23 3HN'
            return rec

        if uprn in ['100022832947', '100022832948', '100022832949']:
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'SE6 4PL'
            return rec

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)
        if record.polling_place_id == '14384':
            rec['location'] = Point(-0.041439, 51.485670, srid=4326)
        return rec
