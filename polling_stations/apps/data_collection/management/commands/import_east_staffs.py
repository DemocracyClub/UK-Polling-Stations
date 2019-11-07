from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E07000193"
    addresses_name = "parl.2019-12-12/Version 1/Democracy Club Polling Districts.csv"
    stations_name = "parl.2019-12-12/Version 1/Democracy Club Polling Stations.csv"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10023784825",  # DE142LF -> DE142LA : 19B Derby Street
            "200001156601",  # DE130PB -> DE130PA : 59 Kitling Greaves Lane
            "10009259693",  # DE130PA -> DE130PB : 64 Kitling Greaves Lane
            "200001155854",  # DE142PG -> DE142PQ : 63A Dallow Street
            "10090989108",  # DE143FY -> DE143FZ : 19 Hornbeam Way, Branston
            "100031654750",  # DE139HE -> DE139BG : Woodside House, Church Road, Rolleston on Dove
            "10008039393",  # DE62HE -> DE62EB : Toll Gate Cottage, Calwich, Mayfield
        ]:
            rec["accept_suggestion"] = True

        return rec

    def station_record_to_dict(self, record):

        if record.stationcode == "BP_45":
            # record = record._replace(polling_place_postcode="")
            record = record._replace(xordinate="422735")
            record = record._replace(yordinate="323640")

        return super().station_record_to_dict(record)
