from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id      = 'E07000143'
    addresses_name  = 'May 2017/BrecklandPropertyPostCodePollingStationWebLookup-2017-02-20.TSV'
    stations_name   = 'May 2017/BrecklandPropertyPostCodePollingStationWebLookup-2017-02-20.TSV'
    elections       = [
        'local.norfolk.2017-05-04',
        #'parl.2017-06-08'
    ]
    csv_delimiter = '\t'

    def station_record_to_dict(self, record):

        """
        File supplied contained obviously inaccurate points
        remove and fall back to geocoding
        """
        if record.pollingplaceid in ['5151', '5370', '5418', '5319']:
            record = record._replace(pollingplaceeasting = '0')
            record = record._replace(pollingplacenorthing = '0')

        return super().station_record_to_dict(record)
