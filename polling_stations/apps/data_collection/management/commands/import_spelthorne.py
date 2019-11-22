from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000213"
    addresses_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-09spel.csv"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-09spel.csv"
    )
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")
        rec = super().address_record_to_dict(record)

        if record.housepostcode in ["TW18 0OO", "TW17 0OO"]:
            return None

        if record.housepostcode == "TW18 3AE":
            rec["postcode"] = "TW153AE"

        if uprn in [
            "33048602",  # TW151AG -> TW152AG : Flat 8, 54 St Michaels Road, Ashford
            "33051119",  # TW178AN -> TW178NF : Bude Haven, Riverside, Penny Lane, Shepperton
            "33040704",  # TW184JQ -> TW184JX : Hengrove Farm, 324B London Road, Ashford
            "33040703",  # TW184JQ -> TW184JX : 324A London Road, Ashford
            "33036070",  # TW182LF -> TW182LE : Towpath House, Riverside Road, Staines-Upon-Thames
        ]:
            rec["accept_suggestion"] = True

        return rec
