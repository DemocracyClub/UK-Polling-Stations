from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000128"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019.tsv"
    elections = ["local.2019-05-02", "europarl.2019-05-23"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):

        if record.polling_place_id == "3393":
            record = record._replace(polling_place_postcode="PR3 0JY")
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-2.800374, 53.926697, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100012423379",  # PR30HA -> PR31QB : Sturzaker House Farm, Stones Lane, Catterall, Preston
            "100012422528",  # PR31NL -> PR31PH : Conway, Lancaster Road, Cabus, Preston
            "100012422994",  # PR30JX -> PR30JU : Brookfold Farm, Park Lane, Forton, Preston
            "10003512835",  # PR30HX -> PR30TB : Keepers Cottage Kirkland Hall Farm, The Avenue, Churchtown
            "10003512836",  # PR30HX -> PR30TB : Kirkland Hall Farm, The Avenue, Churchtown, Preston
            "10034082836",  # PR30LB -> PR30LD : Cogie Hill Farm, Island Lane, Winmarleigh, Preston
            "10003517314",  # FY67SW -> FY68AR : 8 Garstang Road West, Poulton-Le-Fylde
            "10034089363",  # PR31UN -> PR31UL : Brook Cottage, Oakenclough Road, Scorton, Preston
        ]:
            rec["accept_suggestion"] = False

        return rec
