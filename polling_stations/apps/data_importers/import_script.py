class ImportScript:
    def __init__(
        self, council_id, ems, addresses_name, stations_name, elections, encoding
    ):
        self.council_id = council_id
        self.ems = ems
        self.addresses_name = addresses_name
        self.stations_name = stations_name
        self.encoding = encoding
        self.elections = elections

    @property
    def importer_class(self):
        classes = {
            "Idox Eros (Halarose)": "BaseHalaroseCsvImporter",
            "Xpress WebLookup": "BaseXpressWebLookupCsvImporter",
            "Xpress DC": "BaseXpressDemocracyClubCsvImporter",
            "Democracy Counts": "BaseDemocracyCountsCsvImporter",
        }
        return classes[self.ems]

    @property
    def csv_encoding_string(self):
        if self.encoding == "utf-8":
            return ""

        return f'\n    csv_encoding = "{self.encoding}"'

    @property
    def csv_delimiter_string(self):
        if self.addresses_name[-3:] in ("tsv", "TSV"):
            return '\n    csv_delimiter = "\\t"'

        return ""

    @property
    def script(self):
        return f"""from data_importers.management.commands import {self.importer_class}


class Command({self.importer_class}):
    council_id = "{self.council_id}"
    addresses_name = "{self.addresses_name}"
    stations_name = "{self.stations_name}"
    elections = {self.elections}{self.csv_encoding_string}{self.csv_delimiter_string}
"""
