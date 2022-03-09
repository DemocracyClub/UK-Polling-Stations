from django.contrib.gis.geos import Point

from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WRL"
    addresses_name = (
        "2022-05-05/2022-03-09T17:12:14.474461/Democracy_Club__05May2022 v2.CSV"
    )
    stations_name = (
        "2022-05-05/2022-03-09T17:12:14.474461/Democracy_Club__05May2022 v2.CSV"
    )
    elections = ["2022-05-05"]

    def station_record_to_dict(self, record):

        # Marlowe Road URC Hall
        if record.polling_place_id in ["8093", "8089"]:
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-3.050648, 53.417306, srid=4326)
            return rec

        # user issue report #87
        # The Grange Public House
        if record.polling_place_id == "8264":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-3.122875, 53.396797, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "42194110",  # CHARTWELL GAYTON STABLES CHESTER ROAD, GAYTON
            "42200980",  # LIVING ACCOMODATION BIRCHWOOD RESIDENTIAL TREATMENT CENTRE 23-25 BALLS ROAD, OXTON
            "42068483",  # 4 LORNE ROAD, PRENTON
        ]:
            return None

        if record.addressline6 in [
            "CH49 3PG",
            "CH49 2SE",
            "CH62 8AB",
            "CH49 8AB",
            "CH42 9PD",
            "CH60 3RG",
            "CH60 3RA",
            "CH41 0AA",
        ]:
            return None

        return super().address_record_to_dict(record)
