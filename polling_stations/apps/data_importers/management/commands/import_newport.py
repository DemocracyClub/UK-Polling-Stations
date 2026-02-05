from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NWP"
    addresses_name = (
        "2026-05-07/2026-02-05T11:50:52.531977/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-05T11:50:52.531977/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # Cefn Wood Baptist Church, Ebenezer Drive, Rogerstone, Newport, NP10 9DP
        if rec["internal_council_id"] == "13917":
            rec["location"] = Point(327492, 187872, srid=27700)
            return rec

        # Postcode changes pending council confirmation:
        # # 'Eveswell Nursery Unit, St Johns Road, Beechwood, Newport, NP19 8GR' (id: 13791)
        # if record.polling_place_id == "13791":
        #     record = record._replace(polling_place_postcode="NP19 8GX")
        # # 'Llanwern Village Institute, Llanwern Village Institute, Station Road, Llanwern, Newport, NP18 2DW' (id: 13980)
        # if record.polling_place_id == "13980":
        #     record = record._replace(polling_place_postcode="NP18 2DP")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10090274791",  # THE OAKS, FORGE ROAD, BASSALEG, NEWPORT
        ]:
            return None

        if record.post_code in [
            # split
            "NP10 8RL",
            "NP20 2PH",
            "NP10 8NT",
            # suspect
            "NP10 8AT",
            "NP20 3AF",
            "NP20 1LP",
            "NP20 4PL",
        ]:
            return None

        return super().address_record_to_dict(record)
