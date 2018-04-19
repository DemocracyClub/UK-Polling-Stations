from data_collection.management.commands import BaseXpressWebLookupCsvImporter

class Command(BaseXpressWebLookupCsvImporter):
    council_id      = 'E09000004'
    addresses_name  = 'local.2018-05-03/Version 1/PropertyPostCodePollingStationWebLookup-2018-03-21.TSV'
    stations_name   = 'local.2018-05-03/Version 1/PropertyPostCodePollingStationWebLookup-2018-03-21.TSV'
    elections       = ['local.2018-05-03']
    csv_delimiter = '\t'

    def station_record_to_dict(self, record):

        # Correction requested
        if record.pollingplaceid == '843':
            record = record._replace(pollingplaceaddress2 = 'Belmont Road')
            record = record._replace(pollingplaceaddress3 = '')
            record = record._replace(pollingplaceaddress4 = '')
            record = record._replace(pollingplaceaddress5 = '')
            record = record._replace(pollingplaceaddress6 = '')
            record = record._replace(pollingplaceaddress7 = 'DA8 1LB')

        # Point supplied for Footscray Baptist Church is miles off
        if record.pollingplaceid == '869':
            record = record._replace(pollingplaceeasting = '0')
            record = record._replace(pollingplacenorthing = '0')

        # Correction requested
        if record.pollingplaceid == '878':
            record = record._replace(pollingplaceaddress1 = 'Temp Poll Stn (SN1B/E)')
            record = record._replace(pollingplaceaddress2 = 'Reddy Road')
            record = record._replace(pollingplaceaddress3 = 'Slade Green')
            record = record._replace(pollingplaceaddress4 = '')
            record = record._replace(pollingplaceaddress5 = '')
            record = record._replace(pollingplaceaddress6 = '')
            record = record._replace(pollingplaceaddress7 = 'DA8 2AY')
            record = record._replace(pollingplaceeasting = '0')
            record = record._replace(pollingplacenorthing = '0')

        return super().station_record_to_dict(record)
