from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E06000022"
    addresses_name = (
        "local.2019-05-02/Version 1/polling_station_export-2019-03-15BANES.csv"
    )
    stations_name = (
        "local.2019-05-02/Version 1/polling_station_export-2019-03-15BANES.csv"
    )
    elections = ["local.2019-05-02"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        # All of the UPRN data from Bath&NES is a bit dubious.
        # For safety I'm just going to ignore them all
        record = record._replace(uprn="")

        rec = super().address_record_to_dict(record)

        if record.houseid.strip() == "9006798":
            rec["postcode"] = "BS31 2FU"

        if record.houseid.strip() == "9014157":
            rec["postcode"] = "BS14 0FJ"

        if record.houseid.strip() == "9014290":
            rec["postcode"] = "BS14 0FH"

        if record.houseid.strip() == "9002893":
            rec["postcode"] = "BA2 0LH"

        if record.houseid.strip() == "9014583":
            rec["postcode"] = "BS31 2FZ"

        if record.pollingstationnumber == "n/a":
            return None

        if record.housepostcode.strip() == "BS14 0FG":
            return None

        return rec
