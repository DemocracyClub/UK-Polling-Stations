from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E09000015'
    addresses_name = 'parl.2017-06-08/Version 1/Democracy_Club__08June2017 (19).tsv'
    stations_name = 'parl.2017-06-08/Version 1/Democracy_Club__08June2017 (19).tsv'
    elections = ['parl.2017-06-08']
    csv_delimiter = '\t'

    def station_record_to_dict(self, record):

        if record.polling_place_name[-1] == ',':
            record = record._replace(polling_place_name = record.polling_place_name[:-1])

        return super().station_record_to_dict(record)
