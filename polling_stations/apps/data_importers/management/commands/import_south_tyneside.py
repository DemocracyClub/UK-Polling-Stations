from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "STY"
    addresses_name = "2023-05-04/2023-03-09T15:03:06.116940/Democracy_Club__04May2023_South Tyneside.tsv"
    stations_name = "2023-05-04/2023-03-09T15:03:06.116940/Democracy_Club__04May2023_South Tyneside.tsv"
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100000322715",  # 72 BEACH ROAD, SOUTH SHIELDS
            "200000000962",  # 2 CLIFF COTTAGES, QUAY CORNER AVENUE, JARROW
            "200000000963",  # CLIFF HOUSE, QUAY CORNER AVENUE, JARROW
            "200000000961",  # 1 CLIFF COTTAGES, QUAY CORNER AVENUE, JARROW
            "200000000543",  # MANAGERS ACCOMMODATION PUBLIC HOUSE 1 BLACKETT STREET, HEBBURN
            "200000000814",  # THE SCHOOL HOUSE, CAMPBELL PARK ROAD, HEBBURN
            "103001354",  # MANAGERS ACCOMMODATION THE STORYBOOK ABINGDON WAY, SOUTH TYNESIDE, BOLDON COLLIERY
            "200000006403",  # THE COTTAGE, WHITBURN MOORS FARM, SUNDERLAND ROAD, SUNDERLAND
        ]:
            return None

        if record.addressline6 in ["NE31 2XF", "NE34 8AE"]:  # splits
            return None

        return super().address_record_to_dict(record)
