from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RCC"
    addresses_name = (
        "2024-05-02/2024-03-27T08:05:02.256536/Democracy_Club__02May2024.CSV"
    )
    stations_name = (
        "2024-05-02/2024-03-27T08:05:02.256536/Democracy_Club__02May2024.CSV"
    )
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "TS10 4AJ",
            "TS6 0PA",
            # suspect
            "TS7 9HR",
        ]:
            return None

        return super().address_record_to_dict(record)
