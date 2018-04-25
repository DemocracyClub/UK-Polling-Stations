from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id      = 'E07000177'
    addresses_name  = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 Cherwell.tsv'
    stations_name   = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 Cherwell.tsv'
    elections       = ['local.2018-05-03']
    csv_delimiter   = '\t'

    def station_record_to_dict(self, record):

        if record.polling_place_id == '16209':
            record = record._replace(polling_place_easting='445258')
            record = record._replace(polling_place_northing='240545')

        if record.polling_place_id == '16299':
            record = record._replace(polling_place_easting='456935')
            record = record._replace(polling_place_northing='222867')

        if record.polling_place_id == '16372':
            record = record._replace(polling_place_easting='435614')
            record = record._replace(polling_place_northing='237845')

        if record.polling_place_id == '16339':
            record = record._replace(polling_place_easting='442908')
            record = record._replace(polling_place_northing='241900')

        if record.polling_place_id == '16369':
            record = record._replace(polling_place_easting='438592')
            record = record._replace(polling_place_northing='240178')

        if record.polling_place_id == '16455':
            record = record._replace(polling_place_easting='458727')
            record = record._replace(polling_place_northing='231062')

        if record.polling_place_id == '16504':
            record = record._replace(polling_place_easting='449651')
            record = record._replace(polling_place_northing='212578')

        if record.polling_place_id == '16516':
            record = record._replace(polling_place_easting='449488')
            record = record._replace(polling_place_northing='214376')

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip('0')

        if uprn == '100121287092':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'OX15 0TE'
            return rec

        if uprn == '10011929697':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'OX15 6NF'
            return rec

        if record.addressline6 == 'OX2 8HD':
            return None

        if uprn == '10011875290':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'OX25 4RT'
            return rec

        if uprn == '100121287468':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'OX15 4DB'
            return rec

        return super().address_record_to_dict(record)
