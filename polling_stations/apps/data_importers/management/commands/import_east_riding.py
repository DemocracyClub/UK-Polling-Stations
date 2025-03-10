from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ERY"
    addresses_name = (
        "2025-05-01/2025-03-10T12:35:40.745692/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2025-05-01/2025-03-10T12:35:40.745692/Democracy Club - Polling Stations.csv"
    )
    elections = ["2025-05-01"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10095588833",  # PROVENCE HOUSE, LAVENDER FIELDS, BARMBY MOOR, YORK
            "10095943071",  # FLAT 5, 74 HALLGATE, COTTINGHAM
            "10095590278",  # 48 BLANCHARD AVENUE, BEVERLEY
        ]:
            return None

        if record.postcode in [
            # splits
            "HU18 1EH",
        ]:
            return None

        return super().address_record_to_dict(record)
