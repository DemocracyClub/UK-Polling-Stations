from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SRI"
    addresses_name = (
        "2025-05-01/2025-03-17T10:23:51.105469/Democracy Club - SR data.csv"
    )
    stations_name = "2025-05-01/2025-03-17T10:23:51.105469/Democracy Club - SR data.csv"
    elections = ["2025-05-01"]

    # Ignore warning: Polling station Buckshaw Village Community Centre (2-buckshaw-village-community-centre) is in Chorley Borough
    # Station have correct location, just outside the council border.

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
