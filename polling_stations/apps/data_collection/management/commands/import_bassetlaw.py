from django.contrib.gis.geos import Point
from data_collection.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "E07000171"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019Basset.tsv"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019Basset.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):

        if record.property_urn == "10013978026":
            record = record._replace(addressline6="NG22 0GW")
        if record.property_urn == "10093191105":
            record = record._replace(addressline6="S81 7SN")
        if record.property_urn == "100031282735":
            record = record._replace(addressline6="S80 3NL")

        # All of the UPRN data from Bassetlaw is a bit dubious.
        # For safety I'm just going to ignore them all
        record = record._replace(property_urn="")

        if record.addressline6 in ["DN22 8AH", "DN22 0NP", "DN22 0JZ"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.polling_place_id == "8435":  # Lound Village Hall
            record = record._replace(polling_place_postcode="DN22 8RX")
        if record.polling_place_id == "8431":  # Barnby Moor Village Hall
            record = record._replace(polling_place_postcode="DN22 8QU")
        if record.polling_place_id == "8605":  # End-Gilbert Avenue
            record = record._replace(polling_place_postcode="NG22 0JB")
        if record.polling_place_id == "8391":  # Community Room - Westmorland House
            record = record._replace(polling_place_postcode="DN11 8BY")
        if record.polling_place_id == "8513":  # Kingfisher Walk
            record = record._replace(polling_place_postcode="S81 8TQ")
        if record.polling_place_id == "8346":  # The Butter Market
            record = record._replace(polling_place_postcode="DN22 6DB")
        if record.polling_place_id == "8393":  # Langold Village Hall - Committee Room
            record = record._replace(polling_place_postcode="S81 9SW")
        if record.polling_place_id == "8383":  # Harworth & Bircotes Town Hall
            record = record._replace(polling_place_postcode="DN11 8JP")

        rec = super().station_record_to_dict(record)
        # Manton Parish Hall - correction brought forward from locals.
        if record.polling_place_id == "8538":
            rec["location"] = Point(-1.1105063, 53.2957291, srid=4326)

        return rec
