from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SFT"
    addresses_name = "2024-07-04/2024-07-02T11:08:49.736237/SFT_combined.tsv"
    stations_name = "2024-07-04/2024-07-02T11:08:49.736237/SFT_combined.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "41216055",  # 14A UPPER AUGHTON ROAD, SOUTHPORT
            "41109471",  # ALT GRANGE, GRANGE ROAD, LIVERPOOL
            "41215879",  # 3 COACH HOUSE MEWS, WATERLOO, LIVERPOOL
            "41034321",  # 1 GLADSTONE ROAD, SEAFORTH, LIVERPOOL
            "41006565",  # 114A BEDFORD ROAD, BOOTLE
            "41026136",  # 1 DOWNING ROAD, BOOTLE
            "41069997",  # 50 OXFORD ROAD, BOOTLE
            "41069599",  # 85 ORRELL ROAD, BOOTLE
            "41114470",  # 4 MERCHANT CLOSE, BOOTLE
            "41114489",  # 2 FENTON CLOSE, BOOTLE
            "41125103",  # 18A HALL STREET, SOUTHPORT
            "41125739",  # 85 WADHAM ROAD, LIVERPOOL
            "4112833",  # MERTON CAR DISMANTLERS, 483 HAWTHORNE ROAD, BOOTLE
            "41034322",  # 3 GLADSTONE ROAD, SEAFORTH, LIVERPOOL
            "41034324",  # 5 GLADSTONE ROAD, SEAFORTH, LIVERPOOL
            "41034273",  # GUEST FARM, GIDDYGATE LANE, MELLING, LIVERPOOL
        ]:
            return None

        if record.addressline6 in [
            # splits
            "L23 7TX",
            # looks wrong
            "PR8 3LH",
            "L20 6JY",
        ]:
            return None

        return super().address_record_to_dict(record)
