from data_collection.management.commands import BaseXpressWebLookupCsvImporter


class Command(BaseXpressWebLookupCsvImporter):
    council_id = "E07000128"
    addresses_name = "WyrePropertyPostCodePollingStationWebLookup-2017-03-08 2.CSV"
    stations_name = "WyrePropertyPostCodePollingStationWebLookup-2017-03-08 2.CSV"
    elections = ["local.lancashire.2017-05-04", "parl.2017-06-08"]
