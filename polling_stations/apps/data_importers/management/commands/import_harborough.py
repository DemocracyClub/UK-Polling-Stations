from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAO"
    addresses_name = (
        "2025-05-01/2025-03-24T13:48:52.525136/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-24T13:48:52.525136/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
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
            "LE8 0JX",
            "LE17 6AX",
            "LE16 8TD",
            "LE17 5LE",
            # suspect
            "LE16 9FL",
            "LE16 9FN",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # add missing postcode for: Bruntingthorpe Village Hall, Main Street, Bruntingthorpe, Lutterworth, Leicestershire
        if record.polling_place_id == "8051":
            record = record._replace(polling_place_postcode="LE17 5QF")
        return super().station_record_to_dict(record)
