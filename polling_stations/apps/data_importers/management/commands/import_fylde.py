from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "FYL"
    addresses_name = "2021-02-17T15:08:06.810442/Democracy_Club__06May2021.csv"
    stations_name = "2021-02-17T15:08:06.810442/Democracy_Club__06May2021.csv"
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10091662635",  # 3 CLIFTON GRANGE, BLACKPOOL ROAD, CLIFTON, PRESTON
            "10091662634",  # 2 CLIFTON GRANGE, BLACKPOOL ROAD, CLIFTON, PRESTON
            "10091662636",  # 4 CLIFTON GRANGE, BLACKPOOL ROAD, CLIFTON, PRESTON
            "10091662633",  # 1 CLIFTON GRANGE, BLACKPOOL ROAD, CLIFTON, PRESTON
            "100012753403",  # CLIFTON GRANGE FARM, BLACKPOOL ROAD, CLIFTON, PRESTON
            "100010418002",  # 112 LYTHAM ROAD, FRECKLETON, PRESTON
            "100012753615",  # 72 LYTHAM ROAD, FRECKLETON
            "100012753616",  # 74 LYTHAM ROAD, FRECKLETON
            "100012753872",  # LATE STORE, 64 LYTHAM ROAD, FRECKLETON, PRESTON
            "100012834588",  # 19 LYTHAM ROAD, FRECKLETON, PRESTON
            "100010400412",  # 33D CLIFTON STREET, LYTHAM ST. ANNES
            "100010400410",  # 33B CLIFTON STREET, LYTHAM ST. ANNES
            "100012620652",  # 33A CLIFTON STREET, LYTHAM ST. ANNES
            "100012620038",  # 18C CHURCH ROAD, ST. ANNES, LYTHAM ST. ANNES
            "10023481816",  # 10 WYRE STREET, ST. ANNES, LYTHAM ST. ANNES
            "100012753789",  # 50 SEA VIEW RESIDENTIAL PARK BANK LANE, BRYNING WITH WARTON
            "10013594617",  # 4 ARLINGTON HOUSE 342 CLIFTON DRIVE NORTH, LYTHAM ST ANNES
            "100010418049",  # 21A LYTHAM ROAD, FRECKLETON, PRESTON
            "10091661148",  # 21B LYTHAM ROAD, FRECKLETON, PRESTON
        ]:
            return None

        return super().address_record_to_dict(record)
