from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E09000031'
    addresses_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 Waltham Forest.tsv'
    stations_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 Waltham Forest.tsv'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'

    def station_record_to_dict(self, record):

        # Postcode supplied for Downsell Primary School is incorrect
        if record.polling_place_id == '2989':
            record = record._replace(polling_place_postcode='E15 2BS')

        rec = super().station_record_to_dict(record)

        # better point for Mission Grove South Site
        if record.polling_place_id == '2820':
            rec['location'] = Point(-0.025035, 51.581813, srid=4326)

        return rec

    def address_record_to_dict(self, record):

        uprn = record.property_urn.strip().lstrip('0')

        if uprn == '10091187735':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'E11 4ED'
            return rec

        if uprn == '200001420963':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'E11 3AA'
            return rec

        if uprn == '10091185796':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'E10 7EA'
            return rec

        if record.addressline6 == 'E17 9BU':
            return None

        if record.addressline6 == 'E10 5PW':
            return None

        if uprn == '200001424667':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'E17 6PR'
            return rec

        if record.addressline6 == 'E10 6EZ':
            return None

        return super().address_record_to_dict(record)
