from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "OXO"
    addresses_name = (
        "2022-05-05/2022-03-18T12:19:37.382883/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-18T12:19:37.382883/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Baptist Church Room, Godstow Road, Wolvercote
        if record.polling_place_id == "6024":
            record = record._replace(polling_place_postcode="OX2 8PG")

        # Littlemore Community Centre, Giles Road
        if record.polling_place_id == "5833":
            record = record._replace(polling_place_postcode="OX4 4NW")

        rec = super().station_record_to_dict(record)

        # more accurate point for St Alban's Hall
        if rec["internal_council_id"] == "6233":
            rec["location"] = Point(-1.232920, 51.740993, srid=4326)

        # and for Oxford Centre for Mission Studies
        if rec["internal_council_id"] == "6210":
            rec["location"] = Point(-1.264263, 51.764185, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        if record.addressline6 in ["OX3 0TX", "OX4 4QT", "OX4 4UU"]:
            return None

        return super().address_record_to_dict(record)
