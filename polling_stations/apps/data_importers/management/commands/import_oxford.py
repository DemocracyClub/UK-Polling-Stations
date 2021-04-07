from django.contrib.gis.geos import Point
from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "OXO"
    addresses_name = (
        "2021-03-31T10:27:40.155200/Oxford City Polling station  finder.tsv"
    )
    stations_name = "2021-03-31T10:27:40.155200/Oxford City Polling station  finder.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Baptist Church Room, Godstow Road, Wolvercote
        if record.polling_place_id == "5635":
            record = record._replace(polling_place_postcode="OX2 8PG")

        # Aspire, Former St Thomas School, Osney Lane
        if record.polling_place_id == "5845":
            record = record._replace(polling_place_postcode="OX1 1NJ")

        # Littlemore Community Centre, Giles Road
        if record.polling_place_id == "5833":
            record = record._replace(polling_place_postcode="OX4 4NW")

        # Franca`s Cafe 5 Atkyns Road
        if record.polling_place_id == "5767":
            record = record._replace(polling_place_postcode="OX3 8RA")

        rec = super().station_record_to_dict(record)
        # more accurate point for St Alban's Hall
        if rec["internal_council_id"] == "5710":
            rec["location"] = Point(-1.232920, 51.740993, srid=4326)

        # Oxford Centre for Mission Studies
        if rec["internal_council_id"] == "5658":
            rec["location"] = Point(-1.264263, 51.764185, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100121299871",  # 287 COWLEY ROAD, OXFORD
            "100120813508",  # 289 COWLEY ROAD, OXFORD
            "100120846003",  # FLAT 2, 291 COWLEY ROAD, OXFORD
            "100121299714",  # FLAT 1, 291 COWLEY ROAD, OXFORD
            "200004685935",  # GARDEN FLAT 291 COWLEY ROAD, OXFORD
            "10013991228",  # CARETAKERS FLAT UNIVERSITY COLLEGE BOATHOUSE ABINGDON ROAD, OXFORD
            "100120846785",  # BEEFEATER RESTAURANTS, THE MITRE, 18 HIGH STREET, OXFORD
            "200004684441",  # STAFF COTTAGES LADY MARGARET HALL NORHAM GARDENS, OXFORD
            "100121296008",  # LADY MARGARET HALL, NORHAM GARDENS, OXFORD
            "200004676608",  # 83 BANBURY ROAD, OXFORD
            "200004685248",  # 147A COWLEY ROAD, OXFORD
            "10091102602",  # WARDENS FLAT SIR GEOFFREY ARTHUR BUILDING LONG FORD CLOSE, OXFORD
        ]:
            return None

        if record.addressline6 in [
            "OX1 1SR",
            "OX2 7AJ",
            "OX1 4AX",
            "OX4 4UU",
            "OX4 1XG",
            "OX2 0AA",
            "OX4 4QT",
            "OX4 3QD",
            "OX4 3DQ",
            "OX4 3EA",
            "OX3 0AE",
            "OX3 0TX",
            "OX2 7AH",
            "OX4 2AQ",
            "OX4 1HP",
        ]:
            return None

        return super().address_record_to_dict(record)
