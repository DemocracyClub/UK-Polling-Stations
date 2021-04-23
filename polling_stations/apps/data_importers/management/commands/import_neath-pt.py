from data_importers.management.commands import BaseHalaroseCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseHalaroseCsvImporter):
    council_id = "NTL"
    addresses_name = (
        "2021-03-25T10:36:12.245581/Neath PT polling_station_export-2021-03-23.csv"
    )
    stations_name = (
        "2021-03-25T10:36:12.245581/Neath PT polling_station_export-2021-03-23.csv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def station_record_to_dict(self, record):

        if record.pollingstationname == "St. Joseph's R.C Church Hall":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-3.800506, 51.6536899, srid=4326)
            return rec

        # Godrergraig Workingmens Club Glanyrafon Road Ystalyfera SA9 2HA
        if (
            record.pollingstationnumber == "22"
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
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10009182194",  # FFRWD VALE BUNGALOW, DWR Y FELIN ROAD, NEATH
            "100100609132",  # 35B PENYWERN ROAD, NEATH
            "10009177319",  # MAES MELYN BUNGALOW, DRUMMAU ROAD, SKEWEN, NEATH
            "100101040244",  # 11A REGENT STREET EAST, NEATH
            "100100598607",  # 134 SHELONE ROAD, NEATH
            "10023946967",  # 134A SHELONE ROAD, BRITON FERRY
            "100100600419",  # 113 GNOLL PARK ROAD, NEATH
            "100100991905",  # BROOKLYN, TONMAWR ROAD, PONTRHYDYFEN, PORT TALBOT
            "10009184466",  # CILGARN FARM COTTAGE, CWMAVON, PORT TALBOT
            "10009186526",  # TYN Y CAEAU, MARGAM ROAD, MARGAM, PORT TALBOT
            "10014164971",  # FLAT TYN-Y-CAEAU MARGAM ROAD, MARGAM
            "10009184513",  # 1 ALMS HOUSE, MARGAM, PORT TALBOT
        ]:
            return None

        if record.housepostcode in [
            "SA12 8EP",
            "SA10 9DJ",
            "SA10 6DE",
            "SA11 3PW",
            "SA11 1TS",
            "SA11 1TW",
            "SA12 9ST",
            "SA8 4PX",
            "SA11 3QE",
        ]:
            return None

        return super().address_record_to_dict(record)
