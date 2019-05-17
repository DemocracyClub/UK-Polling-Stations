from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E09000013"
    addresses_name = (
        "europarl.2019-05-23/Version 1/polling_station_export-2019-05-03HF.csv"
    )
    stations_name = (
        "europarl.2019-05-23/Version 1/polling_station_export-2019-05-03HF.csv"
    )
    elections = ["europarl.2019-05-23"]

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn == "34157887":
            rec["postcode"] = "W6 0BY"

        if uprn == "34148072":
            rec["accept_suggestion"] = False

        if record.houseid == "9005968":
            return None

        return rec
