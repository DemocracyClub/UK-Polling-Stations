from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E09000016'
    addresses_name = 'parl.2017-06-08/Version 1/Democracy_Club__08June2017 (3).tsv'
    stations_name = 'parl.2017-06-08/Version 1/Democracy_Club__08June2017 (3).tsv'
    elections = ['parl.2017-06-08']
    csv_delimiter = '\t'

    def station_record_to_dict(self, record):

        """
        File supplied contained obviously inaccurate point
        Replace with correction from council
        """
        if record.polling_place_id == '7145':
            record = record._replace(polling_place_easting = '550712.13')

        return super().station_record_to_dict(record)
