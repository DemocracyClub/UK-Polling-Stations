from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SOS"
    addresses_name = (
        "2026-05-07/2026-03-19T11:32:49.463776/Democracy_Club__07May2026 (4).tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-19T11:32:49.463776/Democracy_Club__07May2026 (4).tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10095537349",  # 190B SOUTHCHURCH ROAD, SOUTHEND-ON-SEA, SS1 2NL
        ]:
            return None

        if record.addressline6 in [
            # split
            "SS9 4RP",
            "SS9 1QY",
            "SS9 5EW",
            "SS9 1LN",
            "SS9 1NH",
            "SS3 9QH",
            "SS1 3DR",
            "SS1 2RD",
        ]:
            return None

        return super().address_record_to_dict(record)
