from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RDB"
    addresses_name = (
        "2024-05-02/2024-02-20T16:50:55.903244/Democracy_Club__02May2024.CSV"
    )
    stations_name = (
        "2024-05-02/2024-02-20T16:50:55.903244/Democracy_Club__02May2024.CSV"
    )
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "IG5 0FF",
        ]:
            return None

        return super().address_record_to_dict(record)
