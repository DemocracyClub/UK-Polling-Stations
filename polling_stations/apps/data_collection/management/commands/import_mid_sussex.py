from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000228"
    addresses_name = (
        "2020-02-24T14:06:28.311616/Mid Sussex Polling Station Export - 07.05.2020.tsv"
    )
    stations_name = (
        "2020-02-24T14:06:28.311616/Mid Sussex Polling Station Export - 07.05.2020.tsv"
    )
    elections = ["2020-05-07"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        if (
            record.polling_place_id == "3189"
        ):  # Church Hall, St Edward the Confessor Church, Royal George Road, Burgess Hill
            rec["location"] = Point(-0.14863, 50.96048, srid=4326)
        if (
            record.polling_place_id == "3125"
        ):  # Haywards Heath Baptist Church, Sussex Road, Haywards Heath
            rec["location"] = Point(-0.10036, 50.99487, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6 == "RH16 4RN":
            return None

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
