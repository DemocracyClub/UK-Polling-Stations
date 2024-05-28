from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NKE"
    addresses_name = "2024-07-04/2024-05-29T11:24:30.694292/NKE_combined.tsv"
    stations_name = "2024-07-04/2024-05-29T11:24:30.694292/NKE_combined.tsv"
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # splits
            "NG34 8AA",
        ]:
            return None

        return super().address_record_to_dict(record)
