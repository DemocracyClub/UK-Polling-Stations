from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SRI"
    addresses_name = "2024-07-04/2024-06-10T14:32:56.226915/combined.csv"
    stations_name = "2024-07-04/2024-06-10T14:32:56.226915/combined.csv"
    elections = ["2024-07-04"]

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
