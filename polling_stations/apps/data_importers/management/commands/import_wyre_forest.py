from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WYE"
    addresses_name = "2025-05-01/2025-04-07T11:04:37.863398/Wyre Forest Democracy_Club__01May2025.CSV"
    stations_name = "2025-05-01/2025-04-07T11:04:37.863398/Wyre Forest Democracy_Club__01May2025.CSV"
    elections = ["2025-05-01"]

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "DY11 5QT",
            "DY10 3TF",
            "DY13 8XF",
            "DY10 1LS",
            "DY12 2TN",
            "DY10 3HJ",
            # suspect
            "DY10 2FG",
            "DY11 6FG",
        ]:
            return None
        return super().address_record_to_dict(record)
