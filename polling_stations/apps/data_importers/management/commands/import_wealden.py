from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WEA"
    addresses_name = (
        "2023-05-04/2023-03-11T18:58:22.401719/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-11T18:58:22.401719/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "BN27 1DQ",
            "TN21 0BA",
        ]:
            return None

        return super().address_record_to_dict(record)
