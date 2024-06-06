from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "FAR"
    addresses_name = "2024-07-04/2024-06-14T13:14:35.522442/FAR_combined.tsv"
    stations_name = "2024-07-04/2024-06-14T13:14:35.522442/FAR_combined.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "PO16 7LR",  # split
        ]:
            return None

        return super().address_record_to_dict(record)
