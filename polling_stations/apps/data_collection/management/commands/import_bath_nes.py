from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E06000022"
    addresses_name = (
        "europarl.2019-05-23/Version 1/polling_station_export-2019-05-10Bath.csv"
    )
    stations_name = (
        "europarl.2019-05-23/Version 1/polling_station_export-2019-05-10Bath.csv"
    )
    elections = ["europarl.2019-05-23"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        if record.houseid.strip() == "9006798":
            rec["postcode"] = "BS31 2FU"

        if record.houseid.strip() == "9014157":
            rec["postcode"] = "BS14 0FJ"

        if record.houseid.strip() == "9014290":
            rec["postcode"] = "BS14 0FH"

        if record.houseid.strip() == "9002893":
            rec["postcode"] = "BA2 0LH"

        if record.pollingstationnumber == "n/a":
            return None

        if record.housepostcode.strip() == "BS14 0FG":
            return None

        if record.uprn.strip() == "10001146303":
            rec["accept_suggestion"] = False

        if record.houseid.strip() == "9014616":
            rec["accept_suggestion"] = True

        return rec
