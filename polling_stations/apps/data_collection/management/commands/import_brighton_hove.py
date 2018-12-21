from data_collection.management.commands import BaseXpressWebLookupCsvImporter


class Command(BaseXpressWebLookupCsvImporter):
    council_id = "E06000043"
    addresses_name = "parl.2017-06-08/Version 1/PropertyPostCodePollingStationWebLookup-2017-05-08.TSV"
    stations_name = "parl.2017-06-08/Version 1/PropertyPostCodePollingStationWebLookup-2017-05-08.TSV"
    elections = ["parl.2017-06-08"]
    csv_delimiter = "\t"
