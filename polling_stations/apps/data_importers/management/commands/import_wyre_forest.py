from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WYE"
    addresses_name = (
        "2024-07-04/2024-06-24T10:18:50.159000/Democracy_Club__04July2024.CSV"
    )
    stations_name = (
        "2024-07-04/2024-06-24T10:18:50.159000/Democracy_Club__04July2024.CSV"
    )
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "DY10 1LS",
            "DY10 3TF",
            "DY10 3HJ",
            "DY11 5QT",
            "DY12 2TN",
            # suspect
            "DY10 2FG",  # MILL PARK MEWS, KIDDERMINSTER
        ]:
            return None
        return super().address_record_to_dict(record)
