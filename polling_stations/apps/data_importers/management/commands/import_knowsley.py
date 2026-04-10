from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KWL"
    addresses_name = (
        "2026-05-07/2026-04-10T09:56:45.082831/Democracy_Club__07May2026.CSV"
    )
    stations_name = (
        "2026-05-07/2026-04-10T09:56:45.082831/Democracy_Club__07May2026.CSV"
    )
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # splits
            "L35 5BH",
        ]:
            return None

        return super().address_record_to_dict(record)
