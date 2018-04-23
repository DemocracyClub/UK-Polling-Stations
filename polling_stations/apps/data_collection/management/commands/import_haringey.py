from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E09000014'
    addresses_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 Haringey.tsv'
    stations_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 Haringey.tsv'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip('0')

        if uprn == '10022938046':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'N4 1JZ'
            return rec

        if record.addressline6 == 'N8 8JP' and record.addressline2 == '8 Hornsey Park Road':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'N8 0JP'
            return rec

        if record.addressline6 == 'N22 5JH' and record.addressline2 == '176 Mount Pleasant Road':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'N17 6JQ'
            return rec

        if uprn == '10003982605':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'N22 5AD'
            return rec

        if record.addressline6 == 'N15 5DJ' and record.addressline2 == '45A Broad Lane':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'N15 4DJ'
            return rec

        if record.addressline6 == 'N17 6PF' and record.addressline2 == '36 Downhills Park Road':
            rec = super().address_record_to_dict(record)
            rec['postcode'] = 'N17 6PD'
            return rec

        return super().address_record_to_dict(record)
