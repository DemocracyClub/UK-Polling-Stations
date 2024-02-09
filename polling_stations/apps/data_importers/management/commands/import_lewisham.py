from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "LEW"
    addresses_name = (
        "2024-03-07/2024-02-09T14:04:24.009541/Democracy_Club__07March2024.tsv"
    )
    stations_name = (
        "2024-03-07/2024-02-09T14:04:24.009541/Democracy_Club__07March2024.tsv"
    )
    elections = ["2024-03-07"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Beecroft Garden Primary School, Children`s Centre, Dalrymple Road, London SE4 2HB
        if record.polling_place_id == "22485":
            record = record._replace(polling_place_postcode="SE4 2BH")

        # All Saints Community Centre
        if record.polling_place_id == "22543":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-0.048807, 51.476468, srid=4326)
            return rec

        # Catford Wanderers Sports Club Beckenham Hill Road (Homebase entrance) London SE6 2NU
        if record.polling_place_id == "22866":
            record = record._replace(polling_place_postcode="SE6 3NU")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100022832913",  # 5 COACH HOUSE MEWS, LONDON
            "100021935766",  # 128A BREAKSPEARS ROAD, LONDON
            "100021935767",  # 128B BREAKSPEARS ROAD, LONDON
            "100021966017",  # 32 HALESWORTH ROAD, LONDON
            "100021957981",  # PADDY POWER, 299 EVELYN STREET, LONDON
            "10023226417",  # FLAT 31B, FAIRLAWN MANSIONS, NEW CROSS ROAD, LONDON
            "10023226416",  # FLAT 31A, FAIRLAWN MANSIONS, NEW CROSS ROAD, LONDON
            "100021995184",  # FLAT 4 67 PEPYS ROAD, LONDON
            "100021995183",  # FLAT 3 67 PEPYS ROAD, LONDON
            "100021995182",  # FLAT 2 67 PEPYS ROAD, LONDON
            "100021995181",  # FLAT 1 67 PEPYS ROAD, LONDON
            "100022007329",  # 15 ST. NICHOLAS STREET, LONDON
            "200000563212",  # CEMETERY ATTENDANTS LODGE LADYWELL CEMETERY LADYWELL ROAD, LADYWELL, LONDON
            "200002157666",  # 50B LADYWELL ROAD, LADYWELL, LONDON
            "200002157665",  # 50A LADYWELL ROAD, LADYWELL, LONDON
            "100022010695",  # 11A SYDENHAM ROAD, LONDON
            "100022013147",  # 90 THORPEWOOD AVENUE, LONDON
            "100022013145",  # 86 THORPEWOOD AVENUE, LONDON
        ]:
            return None

        if record.addressline6 in [
            # suspect
            "SE8 5QY",
            "SE14 5UH",
            "SE14 6DS",
            "SE4 1DS",
            "SE4 1DR",
            "SE4 1SX",
            "SE8 4QH",
            "SE13 5DL",
            "SE13 7BD",
            "SE12 9HS",
            "BR1 5PB",
            "SE26 4QZ",
        ]:
            return None

        return super().address_record_to_dict(record)
