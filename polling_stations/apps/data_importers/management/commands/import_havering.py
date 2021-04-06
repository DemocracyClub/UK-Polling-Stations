from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAV"
    addresses_name = "2021-04-05T10:04:15.652473/Democracy_Club__06May2021.tsv"
    stations_name = "2021-04-05T10:04:15.652473/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100021357546",  # 22 WANTZ LANE, RAINHAM
            "10091580271",  # FLAT 1 171 NORTH STREET, ROMFORD
            "10033421338",  # CHO FARM, SOUTHEND ARTERIAL ROAD, UPMINSTER
            "100021383881",  # THE LODGE LODGE LANE, ROMFORD
            "100021357905",  # BRADY SCHOOL HOUSE WENNINGTON ROAD, RAINHAM
            "10091581050",  # 80A LAKE AVENUE, RAINHAM
        ]:
            return None

        if record.addressline6 in [
            "RM11 1DP",
            "RM12 4LG",
            "RM2 6BP",
            "RM7 8DX",
            "RM7 7BX",
            "RM13 9EB",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Upminster Library 26 Corbets Tey Road Upminster RM12 2BB
        if record.polling_place_id == "9178":
            record = record._replace(polling_place_postcode="RM14 2BB")

        # Sapphire Jubilee Community Centre Bolberry Road Collier Row RM5 2FG
        if record.polling_place_id == "8861":
            record = record._replace(polling_place_postcode="RM5 3FG")

        return super().station_record_to_dict(record)
