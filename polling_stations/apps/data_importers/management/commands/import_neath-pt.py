from django.contrib.gis.geos import Point

from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "NTL"
    addresses_name = (
        "2022-05-05/2022-02-28T14:59:06.740989/polling_station_export-2022-02-28.csv"
    )
    stations_name = (
        "2022-05-05/2022-02-28T14:59:06.740989/polling_station_export-2022-02-28.csv"
    )
    elections = ["2022-05-05"]

    def station_record_to_dict(self, record):

        if record.pollingstationname == "St. Joseph's R.C Church Hall":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-3.800506, 51.6536899, srid=4326)
            return rec

        # Godrergraig Workingmens Club Glanyrafon Road Ystalyfera SA9 2HA
        if (
            record.pollingstationnumber == "72"
            and record.pollingstationpostcode == "SA9 2HA"
        ):
            record = record._replace(pollingstationpostcode="SA9 2DE")

        # Dyffryn Clydach Memorial Hall The Drive Longford Neath
        if record.pollingstationname == "Dyffryn Clydach Memorial Hall":
            record = record._replace(pollingstationpostcode="SA10 7HD")

        # Clyne Community Centre Clyne Resolven
        if record.pollingstationname == "Clyne Community Centre":
            record = record._replace(pollingstationpostcode="SA11 4BP")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "SA10 6DE",
            "SA10 9DJ",
            "SA11 1TS",
            "SA11 1TW",
            "SA11 3PW",
            "SA12 8EP",
            "SA8 4PX",
            "SA8 4TS",
        ]:
            return None

        return super().address_record_to_dict(record)
