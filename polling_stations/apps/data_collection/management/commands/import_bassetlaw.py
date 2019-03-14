from django.contrib.gis.geos import Point
from data_collection.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "E07000171"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Basset.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Basset.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):

        if record.property_urn == "10013978026":
            record = record._replace(addressline6="NG22 0GW")

        if record.property_urn == "10093191105":
            record = record._replace(addressline6="S81 7SN")

        # All of the UPRN data from Bassetlaw is a bit dubious.
        # For safety I'm just going to ignore them all
        record = record._replace(property_urn="")

        if record.addressline6 in ["DN22 8AH", "DN22 0NP", "DN22 0JZ"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # Manton Parish Hall
        if record.polling_place_id == "8187":
            rec["location"] = Point(-1.1105063, 53.2957291, srid=4326)

        return rec
