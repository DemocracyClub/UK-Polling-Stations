from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "MAS"
    addresses_name = "2023-05-04/2023-03-23T16:11:56.327479/Eros_SQL_Output005.csv"
    stations_name = "2023-05-04/2023-03-23T16:11:56.327479/Eros_SQL_Output005.csv"
    elections = ["2023-05-04"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10091487792",  # 65 CROMWELL STREET, MANSFIELD
            "10023935274",  # 31 BIRCHLANDS, FOREST TOWN, MANSFIELD
        ]:
            return None

        if record.housepostcode in [
            # Split
            "NG20 0GD",
            "NG18 3FG",
            "NG19 6AT",
        ]:
            return None

        return super().address_record_to_dict(record)
