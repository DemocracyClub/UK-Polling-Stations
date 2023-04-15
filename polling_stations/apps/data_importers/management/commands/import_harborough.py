from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAO"
    addresses_name = "2023-05-04/2023-04-13T08:40:37.550756/Democracy_Club__04May2023 Harborough DC 31UD.tsv"
    stations_name = "2023-05-04/2023-04-13T08:40:37.550756/Democracy_Club__04May2023 Harborough DC 31UD.tsv"
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200001042689",  # THE WELL HOUSE, LUTTERWORTH ROAD, DUNTON BASSETT, LUTTERWORTH
            "200001043348",  # TURNERS BARN FARM, KIBWORTH ROAD, THREE GATES, BILLESDON, LEICESTER
            "10093551160",  # 1D OAKHAM ROAD, TILTON ON THE HILL, LEICESTER
            "10002645475",  # 11 HARBOROUGH ROAD, BILLESDON, LEICESTER
            "200003741786",  # NEWTON GRANGE, TILTON LANE, BILLESDON, LEICESTER
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
        ]:
            return None

        if record.addressline6 in [
            # split
            "LE8 0JX",
            "LE16 9PZ",
            "LE17 6AX",
            "LE17 5LE",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Kibworth Grammar School Hall - Lounge, School Road, Kibworth Beauchamp, Leicestershire, LE8 OEW
        # Postcode mistype, should be a number "0" instead of letter "O"
        if record.polling_place_id == "6240":
            record = record._replace(polling_place_postcode="LE8 0EW")

        # Billesdon Coplow Centre, Uppingham Road, Billesdon, Leicester, LE7 9ER
        # Proposed postcode correction: LE7 9FL
        if record.polling_place_id == "6139":
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)
