from django.contrib.gis.geos import Point
from data_collection.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "E07000171"
    addresses_name = (
        "parl.2019-12-12/Version 2/RevisedDemocracy_Club__12December2019.tsv"
    )
    stations_name = (
        "parl.2019-12-12/Version 2/RevisedDemocracy_Club__12December2019.tsv"
    )
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):

        if record.property_urn == "10013978026":
            record = record._replace(addressline6="NG22 0GW")
        if record.property_urn == "10093191105":
            record = record._replace(addressline6="S81 7SN")
        if record.property_urn == "100031282735":
            record = record._replace(addressline6="S80 3NL")

        # As with Euros I think UPRN data for Bassetlaw was introducing more
        # problems than it was solving. Still safer to ignore.
        record = record._replace(property_urn="")
        rec = super().address_record_to_dict(record)

        if record.addressline6 in [
            "DN22 8AH",
        ]:
            return None

        return rec

    def station_record_to_dict(self, record):
        if record.polling_place_id == "9674":  # Lound Village Hall
            record = record._replace(polling_place_postcode="DN22 8RX")
        if record.polling_place_id == "9670":  # Barnby Moor Village Hall
            record = record._replace(polling_place_postcode="DN22 8QU")
        if record.polling_place_id == "9897":  # End-Gilbert Avenue
            record = record._replace(polling_place_postcode="NG22 0JB")
        if record.polling_place_id == "9632":  # Community Room - Westmorland House
            record = record._replace(polling_place_postcode="DN11 8BY")
        if record.polling_place_id == "9752":  # Kingfisher Walk
            record = record._replace(polling_place_postcode="S81 8TQ")
        if record.polling_place_id == "9832":  # The Butter Market
            record = record._replace(polling_place_postcode="DN22 6DB")
        if record.polling_place_id == "9636":  # Langold Village Hall - Committee Room
            record = record._replace(polling_place_postcode="S81 9SW")
        if record.polling_place_id == "9624":  # Harworth & Bircotes Town Hall
            record = record._replace(polling_place_postcode="DN11 8JP")

        rec = super().station_record_to_dict(record)
        # Manton Parish Hall - correction brought forward from locals.
        if record.polling_place_id == "9777":
            rec["location"] = Point(-1.1105063, 53.2957291, srid=4326)

        return rec
