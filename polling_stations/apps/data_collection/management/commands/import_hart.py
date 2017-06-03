from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000089'
    addresses_name = 'parl.2017-06-08/Version 1/Hart DC General Election polling place 120517.TSV'
    stations_name = 'parl.2017-06-08/Version 1/Hart DC General Election polling place 120517.TSV'
    elections = ['parl.2017-06-08']
    csv_delimiter = '\t'

    def station_record_to_dict(self, record):

        if record.polling_place_id == '1914':
            record = record._replace(polling_place_easting = '479224')
            record = record._replace(polling_place_northing = '154016')

        return super().station_record_to_dict(record)
