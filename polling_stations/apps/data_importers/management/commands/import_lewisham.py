from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "LEW"
    addresses_name = (
        "2026-05-07/2026-03-17T17:36:25.136975/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-17T17:36:25.136975/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Beecroft Garden Primary School, Children`s Centre, Dalrymple Road, London SE4 2HB
        if record.polling_place_id == "25500":
            record = record._replace(polling_place_postcode="SE4 2BH")

        # All Saints Community Centre
        if record.polling_place_id == "25428":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-0.048807, 51.476468, srid=4326)
            return rec

        # Catford Wanderers Sports Club Beckenham Hill Road (Homebase entrance) London SE6 2NU
        if record.polling_place_id == "25418":
            record = record._replace(polling_place_postcode="SE6 3NU")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "100022832913",  # 5 COACH HOUSE MEWS, LONDON
                "100021957981",  # PADDY POWER, 299 EVELYN STREET, LONDON
                "100021995184",  # FLAT 4 67 PEPYS ROAD, LONDON
                "100021995183",  # FLAT 3 67 PEPYS ROAD, LONDON
                "100021995182",  # FLAT 2 67 PEPYS ROAD, LONDON
                "100021995181",  # FLAT 1 67 PEPYS ROAD, LONDON
                "100022007329",  # 15 ST. NICHOLAS STREET, LONDON
                "200002157666",  # 50B LADYWELL ROAD, LADYWELL, LONDON
                "200002157665",  # 50A LADYWELL ROAD, LADYWELL, LONDON
                "100021957009",  # 39 ENNERSDALE ROAD, LONDON
                "100021954384",  # FLAT 19 EASTDOWN COURT 1-11 EASTDOWN PARK, HITHER GREEN, LONDON
                "100021954385",  # FLAT 20 EASTDOWN COURT 1-11 EASTDOWN PARK, HITHER GREEN, LONDON
                "100021954377",  # FLAT 12 EASTDOWN COURT 1-11 EASTDOWN PARK, HITHER GREEN, LONDON
                "100021954375",  # FLAT 10 EASTDOWN COURT 1-11 EASTDOWN PARK, HITHER GREEN, LONDON
                "10090785670",  # FLAT 3 2A MORDEN HILL, LONDON
                "10090785669",  # FLAT 2 2A MORDEN HILL, LONDON
                "10094268956",  # 2 WOODSIDE WALK, FOREST HILL, LONDON
                "10094268955",  # 1 WOODSIDE WALK, LONDON
            ]
        ):
            return None

        if record.addressline6 in [
            # suspect
            "SE8 5QY",
            "SE14 6DS",
            "SE4 1DS",
            "SE4 1DR",
            "SE4 1SX",
            "SE8 4QH",
            "SE13 5DL",
            "SE13 7BD",
            "SE12 9HS",
            "BR1 5PB",
            "BR1 5NE",
            "SE26 4QZ",
            "SE4 1PP",
        ]:
            return None

        return super().address_record_to_dict(record)
