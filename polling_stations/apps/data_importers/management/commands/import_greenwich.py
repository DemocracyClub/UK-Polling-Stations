from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "GRE"
    addresses_name = (
        "2024-10-17/2024-09-18T09:48:05.132507/Democracy_Club__17October2024.CSV"
    )
    stations_name = (
        "2024-10-17/2024-09-18T09:48:05.132507/Democracy_Club__17October2024.CSV"
    )
    elections = ["2024-10-17"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # splits
            "SE9 2BU",
        ]:
            return None

        return super().address_record_to_dict(record)
