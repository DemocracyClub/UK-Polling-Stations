from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000213"
    addresses_name = (
        "local.2019-05-02/Version 1/polling_station_export Spelthorne-2019-02-07.csv"
    )
    stations_name = (
        "local.2019-05-02/Version 1/polling_station_export Spelthorne-2019-02-07.csv"
    )
    elections = ["local.2019-05-02", "europarl.2019-05-23"]
    match_threshold = 98

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in ["33040703", "33040704", "33048602", "33051119"]:
            rec = super().address_record_to_dict(record)
            rec["accept_suggestion"] = True
            return rec

        return super().address_record_to_dict(record)
