from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000238"
    addresses_name = "parl.2019-12-12/Version 2/Democracy Club 08.11.tsv"
    stations_name = "parl.2019-12-12/Version 2/Democracy Club 08.11.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        # user issue report #197
        if record.polling_place_id == "6391":  # Northwick Hotel
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-1.942675, 52.090313, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100120707960",  # WR90BG -> WR98LW : 1 Ford Cottages, Crutch Lane, Elmbridge, Droitwich Spa, Worcs
            "100120707957",  # WR90BD -> WR90BG : The Granary Park Farm, Crutch Lane, Elmbridge, Droitwich Spa, Worcs
            "100120716820",  # WR74PB -> WR74DB : Waterloo House, Alcester Road, Flyford Flavell, Worcs
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10013941784",  # WR90AA -> WR90AG : Bungalow Droitwich High School, Briar Mill, Droitwich Spa, Worcs
        ]:
            rec["accept_suggestion"] = False

        return rec
