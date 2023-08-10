from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "LEW"
    addresses_name = (
        "2022-05-05/2022-02-23T11:33:32.920251/Democracy_Club__05May2022 - Lewisham.tsv"
    )
    stations_name = (
        "2022-05-05/2022-02-23T11:33:32.920251/Democracy_Club__05May2022 - Lewisham.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Sir Francis Drake Primary School
        if record.polling_place_id == "19929":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-0.041453, 51.485092, srid=4326)
            return rec

        # All Saints Community Centre
        if record.polling_place_id == "20137":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-0.048807, 51.476468, srid=4326)
            return rec

        # Catford Wanderers Sports Club Beckenham Hill Road (Homebase entrance) London SE6 2NU
        if record.polling_place_id == "20127":
            record = record._replace(polling_place_postcode="SE6 3NU")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100022832913",  # 5 COACH HOUSE MEWS, LONDON
            "100021978708",  # 299 LEWISHAM HIGH STREET, HITHER GREEN, LONDON
            "100021935766",  # 128A BREAKSPEARS ROAD, LONDON
            "100021935767",  # 128B BREAKSPEARS ROAD, LONDON
            "100021966017",  # 32 HALESWORTH ROAD, LONDON
            "100021957981",  # PADDY POWER, 299 EVELYN STREET, LONDON
        ]:
            return None

        if record.addressline6 in [
            "SE8 3GQ",
            "SE4 1DR",
            "SE4 1DS",
            "SE4 1DR",
            "SE8 5NH",
            "SE8 5NP",
            "BR1 5PB",
        ]:
            return None

        return super().address_record_to_dict(record)
