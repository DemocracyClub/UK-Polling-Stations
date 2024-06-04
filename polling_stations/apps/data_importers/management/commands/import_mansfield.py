from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "MAS"
    addresses_name = "2024-07-04/2024-06-04T15:33:34.031516/Eros_SQL_Output006 (2).csv"
    stations_name = "2024-07-04/2024-06-04T15:33:34.031516/Eros_SQL_Output006 (2).csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10091487792",  # 65 CROMWELL STREET, MANSFIELD
            "10023935274",  # 31 BIRCHLANDS, FOREST TOWN, MANSFIELD
            "10096388538",  # 72 BIFROST BOULEVARD, WARSOP
            "10096388523",  # 17 KEMPTON ROAD, MANSFIELD
            "100031396502",  # 66 CHATSWORTH DRIVE, MANSFIELD
        ]:
            return None

        if record.housepostcode in [
            # splits
            "NG19 6AT",
            # looks wrong
            "NG18 4TG",
        ]:
            return None

        return super().address_record_to_dict(record)
