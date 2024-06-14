from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "GRT"
    addresses_name = "2024-07-04/2024-06-14T11:26:01.609485/Eros_SQL_Output001.csv"
    stations_name = "2024-07-04/2024-06-14T11:26:01.609485/Eros_SQL_Output001.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100062134282",  # FLAT 1 30 YORK ROAD, GUILDFORD
        ]:
            return None
        if record.housepostcode in [
            # split
            "GU1 4TJ",
            "GU23 7JL",
            "GU10 1BP",
            # suspect
            "GU5 9QN",
        ]:
            return None

        return super().address_record_to_dict(record)
