from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000148"
    addresses_name = (
        "local.2019-05-02/Version 1/polling_station_export-2019-03-06Norwich.csv"
    )
    stations_name = (
        "local.2019-05-02/Version 1/polling_station_export-2019-03-06Norwich.csv"
    )
    elections = ["local.2019-05-02", "europarl.2019-05-23"]

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if record.housepostcode.strip() in ["NR4 7FW", "RG8 0RR"]:
            return None

        if record.housepostcode.strip() == "NR3 4EB":
            # this one is just.. odd
            return None

        if uprn in [
            "100091553263"  # NR23AT -> NR23AU : ST JOHNS HOUSE 38 HEIGHAM ROAD, NORWICH
        ]:
            rec["accept_suggestion"] = True

        return rec
