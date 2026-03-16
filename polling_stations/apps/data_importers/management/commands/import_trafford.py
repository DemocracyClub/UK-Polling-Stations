from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TRF"
    addresses_name = (
        "2026-05-07/2026-03-16T10:43:43.906401/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-16T10:43:43.906401/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10070405338",  # 183A CROSS STREET, SALE
        ]:
            return None

        if record.addressline6 in [
            # split
            "WA14 4AN",
            "M33 2BT",
            "M33 3GG",
            # confusing
            "WA15 8TR",
            "M32 8GN",
        ]:
            return None

        return super().address_record_to_dict(record)
