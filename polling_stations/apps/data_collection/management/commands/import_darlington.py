from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000005"
    addresses_name = (
        "europarl.2019-05-23/Version 1/Democracy_Club__23May2019darling.tsv"
    )
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019darling.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        if record.polling_place_id == "5030":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-1.49308179, 54.48766450, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10013315063",  # DL14EP -> DL14ER : Willow Green Care Home, Eastbourne Road, Darlington
            "200002723491",  # DL22XJ -> DL22UF : Elm Bank Cottage, Houghton Bank, Heighington (Part)
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10013312294",  # DL13JU -> DL21RL : Little Burdon Farm, Sadberge
            "10013312299",  # DL13JU -> DL21RL : Little Burdon Farm Cottage, Sadberge
            "200002722478",  # DL13LA -> DL13LB : Orchard House, The Green, Brafferton
            "100110749824",  # DL21QB -> DL21QG : Ivy House, Snipe Lane, Hurworth
            "100110718839",  # DL21QB -> DL22SA : Blackwell Moor Farm, Snipe Lane, Hurworth
            "10013315658",  # DL37LU -> DL11TZ : Managers Accommodation, 17 Post House Wynd, Darlington
        ]:
            rec["accept_suggestion"] = False

        return rec
