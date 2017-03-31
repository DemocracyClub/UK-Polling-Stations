from data_collection.management.commands import BaseHalaroseCsvImporter

class Command(BaseHalaroseCsvImporter):
    council_id      = 'W06000011'
    addresses_name  = 'May 2017/Swansea_polling_station_export-2017-03-06.csv'
    stations_name   = 'May 2017/Swansea_polling_station_export-2017-03-06.csv'
    elections       = ['local.swansea.2017-05-04']
    csv_encoding    = 'latin-1'

    def station_record_to_dict(self, record):

        """
        Joe received correction from Swansea council:

        St. Illtyd's Church
        Ystrad Road
        Fforestfach
        Swansea
        SA5 5AU

        The postcode should be SA5 4BT.
        """
        if record.pollingstationnumber == '72':
            record = record._replace(pollingstationpostcode = 'SA5 4BT')

        return super().station_record_to_dict(record)
