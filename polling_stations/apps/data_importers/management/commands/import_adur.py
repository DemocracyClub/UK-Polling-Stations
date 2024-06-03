from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ADU"
    addresses_name = (
        "2024-07-04/2024-06-03T14:02:23.043501/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-03T14:02:23.043501/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "BN43 6DF",
        ]:
            return None

        return super().address_record_to_dict(record)
