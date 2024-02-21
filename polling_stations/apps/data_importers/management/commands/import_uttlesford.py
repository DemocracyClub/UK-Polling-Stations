from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "UTT"
    addresses_name = (
        "2024-05-02/2024-02-21T15:14:22.604583/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-02-21T15:14:22.604583/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100091278781",  # GREENWOOD, CHURCH ROAD, CHRISHALL, ROYSTON
            "200004270665",  # THE OLD SCHOOL HOUSE STATION ROAD, LITTLE DUNMOW
        ]:
            return None

        if record.addressline6 in [
            # split
            "CB11 4TF",
            "CB10 2ST",
            # suspect
            "CM22 6FG",
            "CM22 6TW",
            "CM6 2FP",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Langley Community Centre, Langley Upper Green, Saffron Walden, CB11 4RU
        if record.polling_place_id == "1582":
            record = record._replace(polling_place_postcode="CB11 4RY")

        # The Community Hall at Carver Barracks, Off Elder Street, Wimbish, Saffron Walden, CB10 2YB
        if record.polling_place_id == "1589":
            record = record._replace(polling_place_postcode="")

        rec = super().station_record_to_dict(record)

        # St. Mary`s CoE Foundation Primary School, Stansted School Hall Hampton Road Stansted CM24 8FE
        if rec["internal_council_id"] == "1707":
            rec["uprn"] = "10090833547"
            rec["location"] = Point(0.19813481644966854, 51.895925525754386, srid=4326)

        # Sewards End Village Hall,	Radwinter Road,	Sewards End	Saffron Walden
        if rec["internal_council_id"] == "1558":
            rec["location"] = Point(0.288313, 52.021565, srid=4326)

        # Hatfield Heath Village Hall, The Heath, Hatfield Heath, Bishop`s Stortford
        if rec["internal_council_id"] == "1632":
            rec["location"] = Point(0.20601490457884916, 51.813635643771676, srid=4326)

        # Hatfield Broad Oak Village Hall,  Cage End, Hatfield Broad Oak, Bishop`s Stortford
        if rec["internal_council_id"] == "1568":
            rec["location"] = Point(0.2420393664199665, 51.82366629430033, srid=4326)

        # St. Mary`s Church Hall,  Birchanger Lane, Birchanger, Bishops Stortford
        if rec["internal_council_id"] == "1705":
            rec["location"] = Point(0.1901025089340043, 51.884113757259236, srid=4326)

        # Farnham Village Hall,  Rectory Lane, Farnham, Bishop`s Stortford
        if rec["internal_council_id"] == "1713":
            rec["location"] = Point(0.14184549037960656, 51.902562759160546, srid=4326)

        # Broxted Village Hall,  Browns End Road, Broxted, Dunmow
        if rec["internal_council_id"] == "1722":
            rec["location"] = Point(0.28619090086472165, 51.90857290858807, srid=4326)

        # Little Canfield Village Hall,  Stortford Road, Little Canfield, Dunmow
        if rec["internal_council_id"] == "1724":
            rec["location"] = Point(0.3075562039168354, 51.868068473426916, srid=4326)

        # Great Easton Village Hall,  Rebecca Meade, Great Easton, Dunmow
        if rec["internal_council_id"] == "1740":
            rec["location"] = Point(0.33530918605452925, 51.90531563768987, srid=4326)

        # Hadstock Village Hall, Church Lane, Hadstock, CB21 4PH
        if rec["internal_council_id"] == "1552":
            rec["location"] = Point(0.27383219315604296, 52.07891625101157, srid=4326)

        return rec
