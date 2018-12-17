from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000008"
    addresses_name = (
        "local.2018-05-03/Version 2/polling_station_export-2018-03-27 Cambridge.csv"
    )
    stations_name = (
        "local.2018-05-03/Version 2/polling_station_export-2018-03-27 Cambridge.csv"
    )
    elections = ["local.2018-05-03"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn == "10090970400":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "CB1 8BN"
            return rec

        return super().address_record_to_dict(record)
