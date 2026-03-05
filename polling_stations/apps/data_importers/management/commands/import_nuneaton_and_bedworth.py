from data_importers.management.commands import BaseXpressWebLookupCsvImporter


class Command(BaseXpressWebLookupCsvImporter):
    council_id = "NUN"
    addresses_name = "2026-05-07/2026-03-05T11:53:55.856561/PropertyPostCodePollingStationWebLookup-2026-03-05.TSV"
    stations_name = "2026-05-07/2026-03-05T11:53:55.856561/PropertyPostCodePollingStationWebLookup-2026-03-05.TSV"
    elections = ["2026-05-07"]
    csv_delimiter = "\t"
