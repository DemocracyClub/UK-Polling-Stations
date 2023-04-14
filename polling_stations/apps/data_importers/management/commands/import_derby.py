from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DER"
    addresses_name = (
        "2023-05-04/2023-04-14T09:07:12.674534/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-14T09:07:12.674534/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100030335044",  # 299 MANSFIELD ROAD, DERBY
        ]:
            return None

        if record.addressline6 in [
            # splits
            "DE73 6UF",
            "DE1 3GB",
            "DE21 4HF",
            "DE24 0LU",
            "DE24 3GT",  # GLENTRESS DRIVE, DERBY
            "DE24 3GU",  # DALBEATTIE AVENUE, DERBY
        ]:
            return None

        return super().address_record_to_dict(record)
