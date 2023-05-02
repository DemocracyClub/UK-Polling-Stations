from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DER"
    addresses_name = (
        "2023-05-04/2023-05-02T22:25:28.393162/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-05-02T22:25:28.393162/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # splits
            "DE73 6UF",
            "DE22 3GT",
            "DE21 4HF",
            "DE24 0LU",
            "DE1 3GB",
        ]:
            return None

        return super().address_record_to_dict(record)
