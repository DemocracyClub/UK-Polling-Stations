from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000228"
    addresses_name = (
        "europarl.2019-05-23/Version 1/Democracy_Club__23May2019 Mid Sussex.tsv"
    )
    stations_name = (
        "europarl.2019-05-23/Version 1/Democracy_Club__23May2019 Mid Sussex.tsv"
    )
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        if record.polling_place_id == "2427":
            rec["location"] = Point(-0.203007, 51.083493, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10070622514"  # RH162QB -> RH162QE : 2 Diamond Cottages, Snowdrop Lane, Lindfield, Haywards Heath, West Sussex
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10070641062",  # RH104HU -> RH104HQ : The Granary, Down Park Farm, Sandy Lane, Crawley Down, Crawley, West Sussex
            "10070644408",  # RH164SA -> RH164RY : Shelter Belt Cottage, Heaselands, Isaacs Lane, Haywards Heath, West Sussex
            "100062201175",  # RH162QY -> RH162HZ : Hangmans Acre Cottage, Ardingly Road, Lindfield, Haywards Heath, West Sussex
        ]:
            rec["accept_suggestion"] = False

        return rec
