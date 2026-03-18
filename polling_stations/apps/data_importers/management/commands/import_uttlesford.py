from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "UTT"
    addresses_name = (
        "2026-05-07/2026-03-02T16:27:11.458539/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-02T16:27:11.458539/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "200004260145",  # THREE GABLES, NEW COMMON, LITTLE HALLINGBURY, BISHOP'S STORTFORD, CM22 7RT
                "10090836555",  # THREE ACRES, NEW BARN LANE, LITTLE HALLINGBURY, BISHOP'S STORTFORD, CM22 7PR
                "10002182834",  # ANNEXE AT PLEDGDON LODGE BRICK END ROAD, HENHAM, CM22 6BN
                "10094832340",  # THE CART LODGE, ROOKERY LANE, WENDENS AMBO, SAFFRON WALDEN, CB11 4JS
                "200004270665",  # THE OLD SCHOOL HOUSE STATION ROAD, LITTLE DUNMOW
            ]
        ):
            return None

        if record.addressline6 in [
            # suspect
            "CM22 6FG",
            "CM22 6TW",
            "CB11 3US",
            "CM6 2GE",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Station chang from council
        # OLD: Dourdan Pavilion, off the Causeway, Great Dunmow CM6 2AA
        # NEW: The Garden Room, Rear of St.Mary's Church, Church Street, Great Dunmow, CM6 2AE
        if record.polling_place_id == "2476":
            record = record._replace(
                polling_place_name="The Garden Room",
                polling_place_address_1="Rear of St.Mary's Church",
                polling_place_address_2="Church Street",
                polling_place_address_3="Great Dunmow",
                polling_place_postcode="CM6 2AE",
            )

        rec = super().station_record_to_dict(record)

        # St. Mary`s CoE Foundation Primary School, Stansted School Hall Hampton Road Stansted CM24 8FE
        if rec["internal_council_id"] == "2567":
            rec["uprn"] = "10090833547"
            rec["location"] = Point(0.19813481644966854, 51.895925525754386, srid=4326)

        # Sewards End Village Hall,	Radwinter Road,	Sewards End	Saffron Walden
        if rec["internal_council_id"] == "2641":
            rec["location"] = Point(0.288313, 52.021565, srid=4326)

        # Hatfield Heath Village Hall, The Heath, Hatfield Heath, Bishop`s Stortford
        if rec["internal_council_id"] == "2598":
            rec["location"] = Point(0.20601490457884916, 51.813635643771676, srid=4326)

        # Hatfield Broad Oak Village Hall,  Cage End, Hatfield Broad Oak, Bishop`s Stortford
        if rec["internal_council_id"] == "2590":
            rec["location"] = Point(0.2420393664199665, 51.82366629430033, srid=4326)

        # St. Mary`s Church Hall,  Birchanger Lane, Birchanger, Bishops Stortford
        if rec["internal_council_id"] == "2565":
            rec["location"] = Point(0.1901025089340043, 51.884113757259236, srid=4326)

        # Farnham Village Hall,  Rectory Lane, Farnham, Bishop`s Stortford
        if rec["internal_council_id"] == "2573":
            rec["location"] = Point(0.14184549037960656, 51.902562759160546, srid=4326)

        # Broxted Village Hall,  Browns End Road, Broxted, Dunmow
        if rec["internal_council_id"] == "2614":
            rec["location"] = Point(0.28619090086472165, 51.90857290858807, srid=4326)

        # Little Canfield Village Hall,  Stortford Road, Little Canfield, Dunmow
        if rec["internal_council_id"] == "2616":
            rec["location"] = Point(0.3075562039168354, 51.868068473426916, srid=4326)

        # Great Easton Village Hall,  Rebecca Meade, Great Easton, Dunmow
        if rec["internal_council_id"] == "2664":
            rec["location"] = Point(0.33530918605452925, 51.90531563768987, srid=4326)

        # Hadstock Village Hall, Church Lane, Hadstock, CB21 4PH
        if rec["internal_council_id"] == "2635":
            rec["location"] = Point(0.27383219315604296, 52.07891625101157, srid=4326)

        return rec
