from data_importers.management.commands import BaseXpressWebLookupCsvImporter


class Command(BaseXpressWebLookupCsvImporter):
    council_id = "HAO"
    addresses_name = "2024-05-02/2024-02-13T10:54:19.565887/PropertyPostCodePollingStationWebLookup-2024-02-13.TSV"
    stations_name = "2024-05-02/2024-02-13T10:54:19.565887/PropertyPostCodePollingStationWebLookup-2024-02-13.TSV"
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
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
        ]:
            return None

        if record.postcode in [
            # split
            "LE8 0JX",
            "LE17 5LE",
            "LE16 9PZ",
            "LE17 6AX",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Kibworth Grammar School Hall - Lounge, School Road, Kibworth Beauchamp, Leicestershire, LE8 OEW
        # Postcode mistype, should be a number "0" instead of letter "O"
        if record.pollingplaceid in ["7348", "7596"]:
            record = record._replace(pollingplaceaddress7="LE8 0EW")

        # Billesdon Coplow Centre, Uppingham Road, Billesdon, Leicester, LE7 9ER
        # Proposed postcode correction: LE7 9FL
        if record.pollingplaceid == "7501":
            record = record._replace(pollingplaceaddress7="")

        return super().station_record_to_dict(record)
