from django.contrib.gis.geos import Point
from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WBK"
    addresses_name = "2021-04-06T15:21:01.728722/Democracy_Club__06May2021 (1).tsv"
    stations_name = "2021-04-06T15:21:01.728722/Democracy_Club__06May2021 (1).tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Peasemore Village Hall Peasemore RG20 7JE
        if record.polling_place_id == "6161":
            record = record._replace(
                polling_place_postcode="RG20 7JE ", polling_place_address_2=""
            )

        rec = super().station_record_to_dict(record)

        # Holybrook Centre Carters Rise Calcot
        if record.polling_place_id == "6238":
            rec["location"] = Point(-1.025829, 51.441617, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200004735144",  # THE BUNGALOW WILCO POULTRY FARM TIDMARSH LANE, TIDMARSH, READING
            "200002495545",  # HUNTERS MOON, BURYS BANK ROAD, GREENHAM, THATCHAM
        ]:
            return None

        if record.addressline6 in ["RG7 6TP", "RG14 1EP", "RG14 6BY", "RG14 3BP"]:
            return None

        return super().address_record_to_dict(record)
