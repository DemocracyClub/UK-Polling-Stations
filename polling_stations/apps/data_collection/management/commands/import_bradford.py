from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E08000032'
    addresses_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018.tsv'
    stations_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018.tsv'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'

    def station_record_to_dict(self, record):

        if record.polling_place_id == '16388':
            record = record._replace(polling_place_postcode='BD22 0HB')

        if record.polling_place_id == '16396':
            record = record._replace(polling_place_postcode='BD22 7PB')

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip('0')

        if uprn == '100051247950':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'LS29 9QJ'
            return rec

        if uprn == '100051229156':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'BD4 0RP'
            return rec

        if uprn == '10090402073':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'BD16 1HT'
            return rec

        if record.addressline6 == 'BD4 0BA':
            return None

        return super().address_record_to_dict(record)
