from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E09000003"
    addresses_name = (
        "parl.2019-12-12/Version 2/Democracy Club - Polling Districts_UKPGE.csv"
    )
    stations_name = "parl.2019-12-12/Version 2/Democracy Club - Polling Stations_2.csv"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn == "200196535":
            return None

        if record.postcode.strip() in [
            "N3 1QT",
            "NW2 2NA",
            "N11 3DD",
            "EN4 8QZ",
            "EN4 8TF",
            "N12 7FB",
            "N12 7EJ",
        ]:
            return None

        return rec
