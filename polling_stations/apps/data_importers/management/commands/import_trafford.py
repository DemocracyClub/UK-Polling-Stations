from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TRF"
    addresses_name = (
        "2026-07-30/2026-06-22T20:45:32.104295/Democracy_Club__30July2026.tsv"
    )
    stations_name = (
        "2026-07-30/2026-06-22T20:45:32.104295/Democracy_Club__30July2026.tsv"
    )
    elections = ["2026-07-30"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10070405338",  # 183A CROSS STREET, SALE
        ]:
            return None

        if record.addressline6 in [
            # split
            "M33 2BT",
            "M33 3GG",
            "WA14 4AN",
            # confusing
            "M32 8GN",
        ]:
            return None

        return super().address_record_to_dict(record)
