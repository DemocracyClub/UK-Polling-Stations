from data_collection.management.commands import BaseHalaroseCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseHalaroseCsvImporter):
    council_id = "E08000025"
    addresses_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-07brum.csv"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-07brum.csv"
    )
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        if record.pollingstationname == "St Mary and Ambrose Church Hall":
            rec["postcode"] = "B5 7RA"
            rec["location"] = Point(-1.904365, 52.458623, srid=4326)

        # Address update from council.
        # Because the Halarose importer derives the internal_council_id
        # from the station name, we need to make the corresponding change in
        # for the address records.
        if record.pollingstationname == "Naseby Youth & Community Centre":
            rec[
                "internal_council_id"
            ] = f"{record.pollingstationnumber}-pentecostal-city-mission-church"
            rec["postcode"] = "B8 3HE"
            rec["address"] = "Pentecostal City Mission Church, 12 Naseby Road"
            rec["location"] = Point(-1.845480, 52.488614, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip()

        # Address update from council.
        # This results in correct polling_station_id
        if record.pollingstationname == "Naseby Youth & Community Centre":
            record = record._replace(
                pollingstationname="pentecostal-city-mission-church"
            )

        rec = super().address_record_to_dict(record)

        if uprn == "10093745957":
            rec["postcode"] = "B36 8HU"

        if uprn in [
            "100070535261",
            "100070571643",
            "100070571644",
            "100070579715",
            "100071260552",
            "100071268408",
            "100071275624",
            "100071284715",
            "100071295285",
            "100071304433",
            "100071304435",
            "100071304437",
            "100071312419",
            "100071313970",
            "100071313971",
            "100071313972",
            "10023291620",
            "10023291621",
            "10023294690",
            "10023295371",
            "100071308644",
            "10023294691",
            "10023294692",
        ]:
            return None

        if record.housepostcode in [
            "B11 3EY",
            "B13 9BT",
            "B12 0HJ",
            "B27 6BY",
            "B8 2RJ",
            "B38 0BQ",
            "B736XF",
        ]:
            return None

        if record.houseid == "48553":
            return None

        return rec
