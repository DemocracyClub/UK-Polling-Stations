from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E09000011"
    addresses_name = (
        "europarl.2019-05-23/Version 1/polling_station_export-2019-05-01.csv"
    )
    stations_name = (
        "europarl.2019-05-23/Version 1/polling_station_export-2019-05-01.csv"
    )
    elections = ["europarl.2019-05-23"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip()
        rec = super().address_record_to_dict(record)

        if record.houseid == "10006012":
            rec["postcode"] = "SE8 3BU"

        if record.houseid == "2024576":
            rec["postcode"] = "SE9 6UD"

        if record.houseid == "2074605":
            rec["postcode"] = "SE2 0XW"

        if uprn in ["10010247892", "10010256784"]:
            rec["accept_suggestion"] = False

        return rec
