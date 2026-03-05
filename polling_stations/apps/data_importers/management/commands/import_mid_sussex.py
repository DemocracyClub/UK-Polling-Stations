from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MSS"
    addresses_name = (
        "2026-05-07/2026-03-05T10:57:53.154959/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-05T10:57:53.154959/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6.replace("\xa0", " ") in [
            # split
            "RH16 2QB",
            "RH19 4NQ",
            # suspect
            "RH10 4SH",
        ]:
            return None
        return super().address_record_to_dict(record)
