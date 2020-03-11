from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E06000032"
    addresses_name = "2020-02-24T12:00:34.574503/DC - Polling Districts.csv"
    stations_name = "2020-02-24T12:00:34.574503/DC - Polling Stations.csv"
    elections = ["2020-05-07"]

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        uprn = record.uprn.strip().lstrip("0")

        if uprn == "10001037360":
            rec["postcode"] = "LU2 7QG"

        if uprn in [
            "200003273279",  # LU31TL -> LU27AU : SCHOOL HOUSE BARNFIELD COLLEGE, BARNFIELD AVENUE, LUTON
        ]:
            rec["accept_suggestion"] = True

        return rec
