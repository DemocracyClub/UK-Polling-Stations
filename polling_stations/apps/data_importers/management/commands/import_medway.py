from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "MDW"
    addresses_name = "2024-05-02/2024-03-21T14:40:57.823024/Eros_SQL_Output010.csv"
    stations_name = "2024-05-02/2024-03-21T14:40:57.823024/Eros_SQL_Output010.csv"
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100062394561",  # WESTBANK FARM, CAPSTONE ROAD, GILLINGHAM
        ]:
            return None

        if record.housepostcode in [
            "ME8 8DB",  # split
            # suspect
            "ME1 2EZ",
            "ME1 2FD",
        ]:
            return None
        return super().address_record_to_dict(record)
