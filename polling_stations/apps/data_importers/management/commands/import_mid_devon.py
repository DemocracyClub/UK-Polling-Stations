from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MDE"
    addresses_name = (
        "2023-05-04/2023-03-17T16:54:00.659878/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-17T16:54:00.659878/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Chawleigh Jubilee Hall, Chawleigh
        if record.polling_place_id == "10823":
            record = record._replace(
                polling_place_easting="", polling_place_northing=""
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10024639781",  # FOXHOLES FARM, CLAYHIDON, CULLOMPTON
            "10002162361",  # POTTERS, SHILLINGFORD, TIVERTON
            "10093536511",  # RAMSTORLAND STAG VIEW, STOODLEIGH, TIVERTON
            "200004004367",  # CARAVANS 3 AND 4 THREE ACRES UFFCULME ROAD, WILLAND
            "200004004366",  # CARAVANS 1 AND 2 THREE ACRES UFFCULME ROAD, WILLAND
            "200004002192",  # PRIMROSE LODGE, LOXBEARE, TIVERTON
            "10009448630",  # MAYFIELD HOUSE, TEMPLETON, TIVERTON
            "10002165647",  # POUND CASTLE, BICKLEIGH, TIVERTON
            "200004005422",  # GUNSTONE LODGE GUNSTONE PARK ROAD FROM GUNSTONE CROSS TO GUNSTONE MILL CROSS, GUNSTONE
            "200004006381",  # GUNSTONE PARK, GUNSTONE, CREDITON
            "10093533623",  # RAVENS WOOD, YEOFORD, CREDITON
            "10093538401",  # COPSTONE HOUSE, BLACK DOG, CREDITON
        ]:
            return None

        if record.addressline6 in [
            # look wrong
            "EX16 8RA",
        ]:
            return None

        return super().address_record_to_dict(record)
