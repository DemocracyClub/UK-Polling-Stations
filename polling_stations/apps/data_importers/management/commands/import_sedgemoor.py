from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SEG"
    addresses_name = (
        "2022-05-05/2022-03-01T14:24:32.538939/polling_station_export-2022-02-28.csv"
    )
    stations_name = (
        "2022-05-05/2022-03-01T14:24:32.538939/polling_station_export-2022-02-28.csv"
    )
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip()
        if record.housepostcode in [
            "BS26 2DX",
            "BS27 3PA",
            "TA5 2BE",
            "TA5 2PF",
            "TA6 4HB",
            "TA6 5NL",
            "TA6 6GD",
            "TA6 6QH",
            "TA6 6RZ",
            "TA6 7BS",
        ]:
            return None

        if uprn in [
            "10090855892",  # PUT HOUSE, FIDDINGTON, BRIDGWATER, TA51JW
            "100040899479",  # 135A TAUNTON ROAD, BRIDGWATER, TA6 6BD
        ]:
            return None

        return super().address_record_to_dict(record)
