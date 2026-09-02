from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BNH"
    addresses_name = (
        "2026-09-24/2026-09-02T13:02:16.170704/Democracy_Club__24September2026.tsv"
    )
    stations_name = (
        "2026-09-24/2026-09-02T13:02:16.170704/Democracy_Club__24September2026.tsv"
    )
    elections = ["2026-09-24"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):

        if record.addressline6 in [
            # split
            "BN2 9PA",
        ]:
            return None
        return super().address_record_to_dict(record)
