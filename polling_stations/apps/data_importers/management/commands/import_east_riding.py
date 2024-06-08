from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ERY"
    addresses_name = "2024-07-04/2024-06-08T17:09:09.105422/ERYC - Democracy Club - Polling Districts.csv"
    stations_name = "2024-07-04/2024-06-08T17:09:09.105422/ERYC - Democracy Club - Polling Stations.csv"
    elections = ["2024-07-04"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10093602661",  # APARTMENT 26, ROGERSON COURT, SCAIFE GARTH, POCKLINGTON, YORK
            "10095588833",  # PROVENCE HOUSE, LAVENDER FIELDS, BARMBY MOOR, YORK
            "10093602661",  # APARTMENT 26, ROGERSON COURT, SCAIFE GARTH, POCKLINGTON, YORK
        ]:
            return None

        if record.postcode in [
            # splits
            "HU18 1EH",
        ]:
            return None

        return super().address_record_to_dict(record)
