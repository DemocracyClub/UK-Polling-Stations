from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ERY"
    addresses_name = "2024-05-02/2024-03-22T11:00:10.036289/Democracy Club - Polling Districts - PCC.csv"
    stations_name = "2024-05-02/2024-03-22T11:00:10.036289/Democracy Club - Polling Stations - PCC.csv"
    elections = ["2024-05-02"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10093602661",  # APARTMENT 26, ROGERSON COURT, SCAIFE GARTH, POCKLINGTON, YORK
            "10095943069",  # FLAT 3, 74 HALLGATE, COTTINGHAM
            "10095943071",  # FLAT 5, 74 HALLGATE, COTTINGHAM
        ]:
            return None
        return super().address_record_to_dict(record)
