from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SRI"
    addresses_name = "2024-05-02/2024-03-19T15:12:00.400914/Eros_SQL_Output004.csv"
    stations_name = "2024-05-02/2024-03-19T15:12:00.400914/Eros_SQL_Output004.csv"
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "PR5 5AU",  # split
        ]:
            return None

        if record.uprn in [
            "100010637839",  # 73A LIVERPOOL OLD ROAD, WALMER BRIDGE, PRESTON
        ]:
            return None
        return super().address_record_to_dict(record)
