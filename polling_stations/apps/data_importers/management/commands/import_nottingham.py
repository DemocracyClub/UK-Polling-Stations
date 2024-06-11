from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NGM"
    addresses_name = (
        "2024-07-04/2024-06-11T09:50:56.274316/Democracy_Club__04July2024.CSV"
    )
    stations_name = (
        "2024-07-04/2024-06-11T09:50:56.274316/Democracy_Club__04July2024.CSV"
    )
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "NG5 2HL",  # split
        ]:
            return None
        return super().address_record_to_dict(record)
