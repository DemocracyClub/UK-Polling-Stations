from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E06000032"
    addresses_name = "parl.2019-12-12/Version 1/DC - Polling Districts2.csv"
    stations_name = "parl.2019-12-12/Version 1/DC - Polling Stations.csv"
    elections = ["parl.2019-12-12"]
    csv_encoding = "windows-1252"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn == "10001037360":
            rec["postcode"] = "LU2 7QG"
            rec["accept_suggestion"] = False

        if uprn in [
            "200003273279",  # LU31TL -> LU27AU : SCHOOL HOUSE BARNFIELD COLLEGE, BARNFIELD AVENUE, LUTON
        ]:
            rec["accept_suggestion"] = True

        return rec
