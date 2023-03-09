from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BNH"
    addresses_name = (
        "2023-05-04/2023-03-09T15:35:23.204420/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-09T15:35:23.204420/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "22057280",  # 2 COMET WAY, WROUGHTON, SWINDON
        ]:
            return None

        if record.addressline6 in ["BN1 8NF", "BN2 9PA", "BN1 3AE"]:  # splits
            return None

        return super().address_record_to_dict(record)
