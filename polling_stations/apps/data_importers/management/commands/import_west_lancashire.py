from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WLA"
    addresses_name = "2021-04-20T12:09:13.316028/WLBC-Democracy_Club__06May2021.tsv"
    stations_name = "2021-04-20T12:09:13.316028/WLBC-Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10012357451",  # HILLCREST BARN, LEES LANE, DALTON, WIGAN
            "10012340452",  # 257 ELMERS GREEN LANE, DALTON, WIGAN
            "10012344231",  # 143D LIVERPOOL ROAD, BICKERSTAFFE, ORMSKIRK
            "10012343974",  # 1 THE PUMP HOUSE, SCARTH HILL LANE, LATHOM, ORMSKIRK
            "10012343975",  # 2 THE PUMP HOUSE, SCARTH HILL LANE, LATHOM, ORMSKIRK
            "10012343976",  # 3 THE PUMP HOUSE, SCARTH HILL LANE, LATHOM, ORMSKIRK
            "10012343977",  # 4 THE PUMP HOUSE, SCARTH HILL LANE, LATHOM, ORMSKIRK
            "10012356512",  # ANNEX HEYES COTTAGE MEADOW LANE, LATHOM
            "10012357871",  # WILLOW BARN, GREEN LANE, TARLETON, PRESTON
            "10012363739",  # 37 BOLD LANE, AUGHTON, ORMSKIRK
            "10012353358",  # 24 SOUTHPORT ROAD, SCARISBRICK, SOUTHPORT
            "10012348052",  # GREEN LANE FARM, GREEN LANE, TARLETON, PRESTON
            "10012363317",  # FLAT 2 MEANYGATE FARM COMMON LANE, SCARISBRICK
            "10012340398",  # 177A CHAPEL ROAD, HESKETH BANK, PRESTON
            "200002461545",  # DOUGLAS LODGE, CHAPEL ROAD, HESKETH BANK, PRESTON
            "200002854842",  # ASTLAND BARN, CHAPEL ROAD, HESKETH BANK, PRESTON
            "200002471251",  # RIBBLE COTTAGE, CHAPEL ROAD, HESKETH BANK, PRESTON
            "10012348092",  # 5 TATLOCKS GRANGE, ORMSKIRK
        ]:
            return None

        if record.addressline6 in [
            "L40 5BE",
            "L39 2EJ",
            "L40 8JB",
            "L40 9QL",
            "L40 1UA",
            "WN8 8LL",
            "WN8 9HU",
            "WN8 6QG",
            "L40 8HQ",
            "L39 5BP",
            "WN8 0AG",
            "WN8 6SH",
            "WN8 7XA",
            "L39 4QJ",
            "L39 0EG",
            "L40 6JA",
            "PR4 6SE",
            "L39 8SR",
            "L39 1RB",
        ]:
            return None

        return super().address_record_to_dict(record)
