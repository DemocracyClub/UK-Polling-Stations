from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CAS"
    addresses_name = (
        "2026-05-07/2026-04-19T14:20:06.301370/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-04-19T14:20:06.301370/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100090360367",  # 210 KENTS HILL ROAD, BENFLEET
            "100091599588",  # 115 DOWNER ROAD, BENFLEET
            "10004941351",  # 420 DAWS HEATH ROAD, BENFLEET
            "10004941352",  # 422 DAWS HEATH ROAD, BENFLEET
        ]:
            return None
        if record.addressline6 in [
            # split
            "SS7 1HH",
            "SS8 9SL",
            "SS8 7PJ",
            "SS8 8HN",
        ]:
            return None
        return super().address_record_to_dict(record)
