from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BAN"
    addresses_name = (
        "2023-05-04/2023-03-17T12:58:09.181146/Democracy_Club__04May2023.CSV"
    )
    stations_name = (
        "2023-05-04/2023-03-17T12:58:09.181146/Democracy_Club__04May2023.CSV"
    )
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "RG26 3SZ",
        ]:
            return None

        return super().address_record_to_dict(record)
