from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000188"
    addresses_name = "2020-02-03T10:23:47.031505/polling_station_export-2020-01-29.csv"
    stations_name = "2020-02-03T10:23:47.031505/polling_station_export-2020-01-29.csv"
    elections = ["2020-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip()
        rec = super().address_record_to_dict(record)

        if uprn == "10009328603":
            rec["postcode"] = "TA5 1JG"

        if uprn == "200000451332":
            rec["postcode"] = "TA7 0SD"

        if uprn == "200000450011":
            rec["postcode"] = "BS26 2HU"

        if record.housepostcode in [
            "TA5 1NQ",
            "TA5 1JW",
        ]:
            return None

        return rec
