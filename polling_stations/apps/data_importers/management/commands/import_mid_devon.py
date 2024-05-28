from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MDE"
    addresses_name = (
        "2024-07-04/2024-05-28T14:15:09.339060/Democracy_Club__04July2024 MID DEVON.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-28T14:15:09.339060/Democracy_Club__04July2024 MID DEVON.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Chawleigh Jubilee Hall, Chawleigh
        if record.polling_place_id == "11714":
            record = record._replace(
                polling_place_easting="",
                polling_place_northing="",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10024639781",  # FOXHOLES FARM, CLAYHIDON, CULLOMPTON
            "10002162361",  # POTTERS, SHILLINGFORD, TIVERTON
            "200004004367",  # CARAVANS 3 AND 4 THREE ACRES UFFCULME ROAD, WILLAND
            "200004004366",  # CARAVANS 1 AND 2 THREE ACRES UFFCULME ROAD, WILLAND
            "10009448630",  # MAYFIELD HOUSE, TEMPLETON, TIVERTON
            "10002165647",  # POUND CASTLE, BICKLEIGH, TIVERTON
            "10095581422",  # OAKLEIGH BARN, BICKLEIGH, TIVERTON
            "200004005422",  # GUNSTONE LODGE GUNSTONE PARK ROAD FROM GUNSTONE CROSS TO GUNSTONE MILL CROSS, GUNSTONE
            "200004006381",  # GUNSTONE PARK, GUNSTONE, CREDITON
            "10093538401",  # COPSTONE HOUSE, BLACK DOG, CREDITON
            "10009451330",  # TOADYPARK, ZEAL MONACHORUM, CREDITON
            "10093538015",  # HIGHER POND BARN, KEYMELFORD, YEOFORD, CREDITON
            "10002162357",  # RADDS COTTAGE, CALVERLEIGH, TIVERTON
            "10095583600",  # HOLIDAY COTTAGE 1 ROAD FROM PITTON CROSS TO HOOK FARM, CHERITON BISHOP
            "10095583601",  # HOLIDAY COTTAGE 2 ROAD FROM PITTON CROSS TO HOOK FARM, CHERITON BISHOP
        ]:
            return None

        if record.addressline6 in [
            # look wrong
            "EX16 8RA",
        ]:
            return None

        return super().address_record_to_dict(record)
