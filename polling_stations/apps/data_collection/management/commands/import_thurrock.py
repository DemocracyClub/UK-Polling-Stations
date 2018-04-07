from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E06000034'
    addresses_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 (1) Thurrock.tsv'
    stations_name = 'local.2018-05-03/Version 1/Democracy_Club__03May2018 (1) Thurrock.tsv'
    elections = ['local.2018-05-03']
    csv_delimiter = '\t'

    def station_record_to_dict(self, record):

        """
        File supplied contained obviously inaccurate point
        remove it and fall back to geocoding
        """
        if record.polling_place_id == '5323':
            record = record._replace(polling_place_easting = '0')
            record = record._replace(polling_place_northing = '0')

        return super().station_record_to_dict(record)


    def address_record_to_dict(self, record):

        if record.addressline6.strip() == 'SS17 0QT':
            return None

        return super().address_record_to_dict(record)
