from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MSS"
    addresses_name = (
        "2023-05-04/2023-04-24T16:40:02.441254/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-24T16:40:02.441254/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10070621576",  # 1 SAWMILLS COTTAGES, PADDOCKHURST ROAD, TURNERS HILL, CRAWLEY
            "10070641437",  # SHOOTERS LODGE, BRANTRIDGE LANE, BALCOMBE, HAYWARDS HEATH
            "100061873895",  # NORTHLANDS, STAIRBRIDGE LANE, BOLNEY, HAYWARDS HEATH
            "10090944299",  # 10 OLDFIELD DRIVE, HAYWARDS HEATH
            "10090944298",  # 9 OLDFIELD DRIVE, HAYWARDS HEATH
            "10090944297",  # 8 OLDFIELD DRIVE, HAYWARDS HEATH
            "10093413540",  # 7A OLDFIELD DRIVE, HAYWARDS HEATH
            "100062485213",  # 3 ROSE COTTAGES, SNOWDROP LANE, LINDFIELD, HAYWARDS HEATH
        ]:
            return None

        if record.post_code in [
            # splits
            "RH17 7DY",
            "BN6 9NA",
            "RH16 2QB",
            "RH17 7GD",  # PRIMROSE WAY, HAYWARDS HEATH
        ]:
            return None

        return super().address_record_to_dict(record)
