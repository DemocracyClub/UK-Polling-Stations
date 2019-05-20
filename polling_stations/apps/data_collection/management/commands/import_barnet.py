from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E09000003"
    addresses_name = (
        "europarl.2019-05-23/Version 1/Decmoracy Club - Polling Districts.csv"
    )
    stations_name = (
        "europarl.2019-05-23/Version 1/Democracy Club - Polling Stations.csv"
    )
    elections = ["europarl.2019-05-23"]

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn == "200196535":
            rec["accept_suggestion"] = False

        return rec
