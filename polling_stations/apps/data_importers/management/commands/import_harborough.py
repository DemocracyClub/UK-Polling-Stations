from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAO"
    addresses_name = "2024-07-04/2024-06-19T12:01:44.718343/HAO_combined.tsv"
    stations_name = "2024-07-04/2024-06-19T12:01:44.718343/HAO_combined.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10094812143",  # 5 LEAS CLOSE, ULLESTHORPE, LUTTERWORTH
                "200001042689",  # THE WELL HOUSE, LUTTERWORTH ROAD, DUNTON BASSETT, LUTTERWORTH
                "200001043348",  # TURNERS BARN FARM, KIBWORTH ROAD, THREE GATES, BILLESDON, LEICESTER
                "10002645475",  # 11 HARBOROUGH ROAD, BILLESDON, LEICESTER
                "200003738208",  # LAUNDE ABBEY, LAUNDE ROAD, LAUNDE, LEICESTER
                "200003741962",  # WILD MEADOW FARM, BOWDEN LANE, WELHAM, MARKET HARBOROUGH
                "10094809283",  # 119 HARVEST ROAD, MARKET HARBOROUGH
                "10094809286",  # 125 HARVEST ROAD, MARKET HARBOROUGH
                "200003740791",  # WHARF HOUSE, NORTH KILWORTH, LUTTERWORTH
                "10034463148",  # 67A BITTESWELL ROAD, LUTTERWORTH
                "200003736031",  # THE WATER TOWER, BITTESWELL ROAD, LUTTERWORTH
                "100030480044",  # WATERWORKS HOUSE, BITTESWELL ROAD, LUTTERWORTH
                "100030481643",  # MISTERTON FIELDS FARM, MISTERTON, LUTTERWORTH
                "10034458556",  # THE BARN BOSTON LODGE LUTTERWORTH ROAD, GILMORTON
            ]
        ):
            return None

        if record.addressline6 in [
            # split
            "LE16 9PZ",
            "LE8 0JX",
            "LE17 5LE",
            "LE17 6AX",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # postcode correction for: Billesdon Coplow Centre, Uppingham Road, Billesdon, Leicester, LE7 9ER
        # source: https://www.thecoplowcentre.com/contact
        if record.polling_place_id == "7853":
            record = record._replace(polling_place_postcode="LE7 9FL")
        return super().station_record_to_dict(record)
