from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000041'
    addresses_name = 'ExeterDemocracy_Club__04May2017 (2).tsv'
    stations_name = 'ExeterDemocracy_Club__04May2017 (2).tsv'
    elections = [
        'local.devon.2017-05-04',
        'local.exeter.2017-05-04',
        'parl.2017-06-08'
    ]
    csv_delimiter = '\t'

    def station_record_to_dict(self, record):

        """
        File supplied contained obviously inaccurate point
        Joe queried + received correction: 290734, 91778
        """
        if record.polling_place_id == '2883':
            record = record._replace(polling_place_easting = '290734')
            record = record._replace(polling_place_northing = '91778')

        return super().station_record_to_dict(record)
