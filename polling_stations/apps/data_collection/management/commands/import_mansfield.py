from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000174"
    addresses_name = "local.2019-05-02/Version 1/polling_station_export-2019-02-12.csv"
    stations_name = "local.2019-05-02/Version 1/polling_station_export-2019-02-12.csv"
    elections = ["local.2019-05-02"]

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn == "10091484857":
            rec["postcode"] = "NG19 7NH"

        if record.housepostcode == "NG19 0BZ":
            return None

        return rec
