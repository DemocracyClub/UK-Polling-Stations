from data_collection.management.commands import BaseXpressWebLookupCsvImporter


class Command(BaseXpressWebLookupCsvImporter):
    council_id = "E07000110"
    addresses_name = "local.2018-05-03/Version 2/PropertyPostCodePollingStationWebLookup-2018-03-23.TSV"
    stations_name = "local.2018-05-03/Version 2/PropertyPostCodePollingStationWebLookup-2018-03-23.TSV"
    elections = ["local.2018-05-03"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):

        if record.postcode == "ME18 5PB":
            return None

        return super().address_record_to_dict(record)
