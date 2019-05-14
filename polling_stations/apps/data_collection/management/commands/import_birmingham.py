from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E08000025"
    addresses_name = (
        "europarl.2019-05-23/Version 1/polling_station_export-2019-04-30.csv"
    )
    stations_name = (
        "europarl.2019-05-23/Version 1/polling_station_export-2019-04-30.csv"
    )
    elections = ["europarl.2019-05-23"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip()
        rec = super().address_record_to_dict(record)

        if uprn == "100071465044":
            rec["postcode"] = "B44 0NN"

        if uprn == "10093745957":
            rec["postcode"] = "B36 8HU"

        if uprn == "10023294797":
            rec["postcode"] = "B72 1BX"

        if record.housepostcode in ["B11 3EY", "B13 9BT", "B27 6BY"]:
            return None
        if uprn in [
            "100070369867",
            "10090247576",
            "10090247575",
            "10090247574",
            "10090247573",
            "10090247571",
            "10090247570",
            "10090247577",
            "10090247569",
            "10090436086",
        ]:
            return None

        if record.houseid == "48553":
            return None

        return rec
