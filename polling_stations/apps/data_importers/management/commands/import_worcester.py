from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOC"
    addresses_name = (
        "2023-05-04/2023-03-08T12:22:56.608272/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-08T12:22:56.608272/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10090440987",  # FLAT AT THE BEDWARDINE 128 BROMYARD ROAD, WORCESTER
            "100120648786",  # 145A COLUMBIA DRIVE, WORCESTER
            "100120671753",  # 3 TROTSHILL LANE EAST, WORCESTER
        ]:
            return None

        return super().address_record_to_dict(record)
