from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WYR"
    addresses_name = (
        "2024-07-04/2024-05-29T08:48:44.168590/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-29T08:48:44.168590/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10024171572",  # WELL WOOD VIEW, STATION LANE, SCORTON, PRESTON
            "10093999437",  # PLEASANT VIEW, BLACKPOOL ROAD, POULTON-LE-FYLDE
            "10034085598",  # MANOR VALE, ST. MICHAELS ROAD, BILSBORROW, PRESTON
            "100012422216",  # MANOR HOUSE FARM, ST. MICHAELS ROAD, BILSBORROW, PRESTON
            "10034083802",  # FIELDVIEW, PINFOLD LANE, SOWERBY, PRESTON
            "100010717609",  # 41 YORK DRIVE, GREAT ECCLESTON, PRESTON
            "200001037729",  # SHEPHERDS FARM, 771 GARSTANG ROAD, BARTON, PRESTON
            "100012846911",  # THE MOUNT HOTEL THE ESPLANADE, FLEETWOOD
            "10003529935",  # BRIGG HOUSE FARM, LANCASTER ROAD, OUT RAWCLIFFE, PRESTON
            "10003530610",  # THE OLD PRINT WORKS BRUNA HILL, BARNACRE
            "10024173046",  # FORWARD2ME, YORK HOUSE, MANOR PARK, GREEN LANE WEST, GARSTANG, PRESTON
            "10034086401",  # 3 CLEVELEY BRIDGE APARTMENTS CLEVELEY BANK LANE, FORTON
            "10034086399",  # 1 CLEVELEY BRIDGE APARTMENTS CLEVELEY BANK LANE, FORTON
            "10034086400",  # 2 CLEVELEY BRIDGE APARTMENTS CLEVELEY BANK LANE, FORTON
            "100012750892",  # HUMBLESCOUGH FARM, HUMBLESCOUGH LANE, NATEBY, PRESTON
            "100012422799",  # SANS-SOUCI, LONGMOOR LANE, NATEBY, PRESTON
            "10034084730",  # MORRISWOOD, SIX ARCHES LANE, SCORTON, PRESTON
            "10034082835",  # CRAWLEY CROSS COTTAGE, GARSTANG ROAD, WINMARLEIGH, PRESTON
            "10003513068",  # LONGCROFT, WOODS LANE, EAGLAND HILL, PRESTON
            "100012422100",  # PARKERS CLOSE, GREEN DICKS LANE, PILLING, PRESTON
        ]:
            return None

        if record.post_code in [
            # split
            "PR3 6HS",
            # looks wrong
            "FY6 7GH",
            "PR3 1TS",
            "FY6 7BH",
            "PR3 0NT",
            "PR3 0DW",
        ]:
            return None

        return super().address_record_to_dict(record)
