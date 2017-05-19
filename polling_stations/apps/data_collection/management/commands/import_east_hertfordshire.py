from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = 'E07000242'
    addresses_name = 'Democracy_Club__04May2017 (5).CSV'
    stations_name = 'Democracy_Club__04May2017 (5).CSV'
    elections = ['parl.2017-06-08']

    def station_record_to_dict(self, record):

        """
        East Herts Council contacted us to say...
        Change of polling station for the General Election:
        Ware Drill Hall is being replaced by
        3rd Ware Scout Hut, Broadmeads, Ware, SG12 9HY
        """
        if record.polling_place_id == '819':
            record = record._replace(polling_place_name = '3rd Ware Scout Hut')
            record = record._replace(polling_place_address_1 = 'Broadmeads')
            record = record._replace(polling_place_address_2 = 'Ware')
            record = record._replace(polling_place_address_3 = '')
            record = record._replace(polling_place_address_4 = '')
            record = record._replace(polling_place_postcode = 'SG12 9HY')
            record = record._replace(polling_place_easting = '0')
            record = record._replace(polling_place_northing = '0')

        return super().station_record_to_dict(record)
