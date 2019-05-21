from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E09000033"
    addresses_name = (
        "europarl.2019-05-23/Version 1/polling_station_export-2019-05-03.csv"
    )
    stations_name = (
        "europarl.2019-05-23/Version 1/polling_station_export-2019-05-03.csv"
    )
    elections = ["europarl.2019-05-23"]

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if record.houseid == "3007640":
            return None

        if record.houseid == "10009330":  # W9 1QF
            rec["postcode"] = "W9 3QF"

        if record.houseid == "10010095":  # W9 1DL
            rec["postcode"] = "W9 2DL"

        if uprn == "100022801294":
            rec["postcode"] = "W1J 7JJ"

        if uprn == "100023474073":
            rec["postcode"] = "W1J 6HL"

        if uprn == "10033565232":
            rec["postcode"] = "SW7 5HF"

        if uprn == "10033561131":
            rec["postcode"] = "SW1P 4SA"

        if record.houseid == "3075271":
            rec["accept_suggestion"] = False

        if record.houseid == "3036900":
            rec["accept_suggestion"] = False

        if uprn in ["10033578350", "10033578347", "10033578348", "10033578349"]:
            rec["accept_suggestion"] = False

        if record.houseid == "10010622":
            return None

        return rec
