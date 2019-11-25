from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E07000035"
    addresses_name = "parl.2019-12-12/Version 1/Democracy Club - Polling Districts - Derbyshire Dales.csv"
    stations_name = "parl.2019-12-12/Version 1/Democray Club - Polling Stations - Derbyshire Dales.csv"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn in ["10010331972", "10010331834", "10070090689"]:
            rec["accept_suggestion"] = True

        return rec
