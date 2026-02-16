import subprocess


def ruff_format_str(py_script):
    p = subprocess.Popen(
        ["ruff", "format", "-"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    p.stdin.write(py_script)
    stdout, _stderr = p.communicate()
    return stdout


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
            "Idox Eros (Halarose) 2026 Update": "BaseHalarose2026UpdateCsvImporter",
            "Xpress WebLookup": "BaseXpressWebLookupCsvImporter",
            "Xpress DC": "BaseXpressDemocracyClubCsvImporter",
            "Democracy Counts": "BaseDemocracyCountsCsvImporter",
        }
        return classes.get(self.ems, "Unknown")

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
        script_str = f"""from data_importers.management.commands import {self.importer_class}


class Command({self.importer_class}):
    council_id = "{self.council_id}"
    addresses_name = "{self.addresses_name}"
    stations_name = "{self.stations_name}"
    elections = {self.elections}{self.csv_encoding_string}{self.csv_delimiter_string}
"""
        return ruff_format_str(script_str)
