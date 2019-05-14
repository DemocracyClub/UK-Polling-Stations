from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000188"
    addresses_name = (
        "europarl.2019-05-23/Version 1/polling_station_export-2019-05-14.csv"
    )
    stations_name = (
        "europarl.2019-05-23/Version 1/polling_station_export-2019-05-14.csv"
    )
    elections = ["europarl.2019-05-23"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip()
        rec = super().address_record_to_dict(record)

        if uprn == "200000451332":
            rec["postcode"] = "TA7 0SD"

        if uprn == "200000450011":
            rec["postcode"] = "BS26 2HU"

        return rec
