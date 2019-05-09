from data_collection.management.commands import BaseHalaroseCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseHalaroseCsvImporter):
    council_id = "E09000018"
    addresses_name = (
        "europarl.2019-05-23/Version 1/polling_station_export-2019-04-25.csv"
    )
    stations_name = (
        "europarl.2019-05-23/Version 1/polling_station_export-2019-04-25.csv"
    )
    elections = ["europarl.2019-05"]

    def station_record_to_dict(self, record):
        def make_station_id(record):
            number = record.pollingstationnumber
            name = (
                record.pollingstationname.lower()
                .replace(" - ", "-")
                .replace(".", "")
                .replace(",", "")
                .replace("'", "")
                .replace(" ", "-")
            )
            return f"{number}-{name}"

        station_id = make_station_id(record)

        rec = super().station_record_to_dict(record)

        if station_id == "29-caravan-kings-arbour":
            rec["location"] = Point(512063.336, 178157.063, srid=27700)

        if station_id == "86-caravan-worple-avenue":
            rec["location"] = Point(516137.00367345, 174846.99981823, srid=27700)

        if station_id == "70-caravan-at-hounslow-avenue":
            rec["location"] = Point(514069.99983565, 174816.99840605, srid=27700)

        if station_id == "48-caravan-sutton-square":
            rec["location"] = Point(512893.00087335, 176770.99907917, srid=27700)

        if station_id == "73-caravan-outside-146-central-avenue":
            rec["location"] = Point(514712.99917068, 174883.99922726, srid=27700)

        if station_id == "77-caravan-opposite-the-green-school-for-girls-entrance":
            rec["location"] = Point(516489.37, 176818.182, srid=27700)

        if station_id == "32-caravan-the-green":
            rec["location"] = Point(511541.99814156, 176441.00353941, srid=27700)

        if station_id == "40-caravan-entrance-to-beaversfield-park":
            rec["location"] = Point(512123.00286217, 175824.0001548, srid=27700)

        if station_id == "71-caravan-at-hounslow-avenue":
            rec["location"] = Point(514069.99983565, 174816.99840605, srid=27700)

        if station_id == "10-caravan-adjacent-to-clifton-parade":
            rec["location"] = Point(511140.00194252, 171948.99936223, srid=27700)

        return rec

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn == "10091693351":
            rec["postcode"] = "TW80LL"

        if record.houseid == "104146":
            return None
        return rec
