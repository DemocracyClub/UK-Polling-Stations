from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WYE"
    addresses_name = "2024-05-02/2024-04-10T12:56:13.692844/Wyre Forest Democracy_Club__02May2024.CSV"
    stations_name = "2024-05-02/2024-04-10T12:56:13.692844/Wyre Forest Democracy_Club__02May2024.CSV"
    elections = ["2024-05-02"]

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
