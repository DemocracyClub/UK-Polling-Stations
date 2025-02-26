from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "GRA"
    addresses_name = "2025-05-01/2025-02-26T16:12:57.498250/Eros_SQL_Stations.csv"
    stations_name = "2025-05-01/2025-02-26T16:12:57.498250/Eros_SQL_Stations.csv"
    elections = ["2025-05-01"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100060938783",  # 162 OLD ROAD EAST, GRAVESEND
            "100060939369",  # 36-38 OVERCLIFFE, GRAVESEND
            "10012013958",  # WOODHILL FARM, BRIMSTONE HILL, MEOPHAM, GRAVESEND
            "10012014473",  # BRIMSTONE WOOD, BRIMSTONE HILL, MEOPHAM, GRAVESEND
            "10012014411",  # BRIMSTONE LODGE, BRIMSTONE HILL, MEOPHAM, GRAVESEND
            "100060934937",  # PRIMROSE COTTAGE, LEYWOOD ROAD, MEOPHAM, GRAVESEND
        ]:
            return None

        if record.housepostcode.strip() in [
            # suspect
            "DA13 0RN",  # HARVEL ROAD, MEOPHAM, GRAVESEND
            "DA3 7AL",  # SHIPLEY HILL COTTAGES, LONGFIELD ROAD, LONGFIELD
        ]:
            return None

        return super().address_record_to_dict(record)
