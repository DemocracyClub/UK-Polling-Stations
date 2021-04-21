from django.contrib.gis.geos import Point
from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SOL"
    addresses_name = "2021-04-07T11:17:55.688819/Democracy_Club__06May2021.CSV"
    stations_name = "2021-04-07T11:17:55.688819/Democracy_Club__06May2021.CSV"
    elections = ["2021-05-06"]

    def station_record_to_dict(self, record):
        # Whar Hall Road Community Centre's postcode doesn't match AddressBase, but
        # online sources agree with the council. As the postcodes are adjacent, we'll
        # leave this unmodified from what's in the CSV. First noted in 2019, and checked
        # and carried across for 2021.

        # These polling places have a UPRN, and the addressbase postcode doesn't match
        # the postcode from the council. In these cases the addressbase postcode matches
        # the postcode used on the venue's website.
        if record.polling_place_id == "8918":  # KEC Church Centre
            record = record._replace(polling_place_postcode="B37 6NP")
        # Fixes carried forward
        if record.polling_place_id == "8877":  # Barston Memorial Institute
            record = record._replace(polling_place_postcode="B92 0JU")
        if record.polling_place_id == "8907":  # St Clements Church
            record = record._replace(polling_place_postcode="B36 0BA")
        if (
            record.polling_place_id == "9001"
        ):  # The Royal British Legion (Knowle) Club Limited
            record = record._replace(polling_place_postcode="B93 9LU")
        if record.polling_place_id == "9138":  # Woodlands Campus
            record = record._replace(polling_place_postcode="B36 0NF")

        # Fixes carried forward
        # Three Trees Community Centre
        if record.polling_place_id == "8928":
            record = record._replace(polling_place_uprn="100071461342")
        # Dorridge Methodist Church
        if record.polling_place_id == "8945":
            record = record._replace(polling_place_uprn="100071001475")

        rec = super().station_record_to_dict(record)

        # Tudor Grange Leisure Centre
        if record.polling_place_id == "9156":
            rec["location"] = Point(-1.7881577, 52.4124167, srid=4326)

        # Catherine de Barnes Village Hall
        if record.polling_place_id == "8873":
            rec["location"] = Point(-1.7382134, 52.4203089, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        if record.addressline6 in [
            "B37 7WD",  # 10 properties embedded in another area
        ]:
            return None

        if record.addressline6 in [
            "B37 7RN",
            "B37 7HW",
            "B37 7LY",
            "B92 8NA",
            "B93 8PP",
            "B37 6EU",
            "B93 9JN",
            "CV7 7EG",
            "CV7 7DG",
            "CV7 7GY",
            "B91 1UQ",
            "B90 3QQ",
            "B90 3EE",
            "B91 2UN",
            "B91 2BP",
        ]:
            return None  # split

        return rec
