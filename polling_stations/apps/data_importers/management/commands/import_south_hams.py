from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SHA"
    addresses_name = (
        "2023-05-04/2023-03-22T10:41:08.648868/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-22T10:41:08.648868/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10008857241",  # GYPSY LANE SITE, BUCKFASTLEIGH
            "10008919040",  # LUDD FARM, UGBOROUGH, IVYBRIDGE
            "10008919308",  # THORNBROOK, THURLESTONE SANDS, KINGSBRIDGE
            "100040274671",  # BRITANNIA HOUSE, COLLEGE WAY, DARTMOUTH
            "10008912570",  # WILLANDS, MODBURY, IVYBRIDGE
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # Sherford Community Hub, Hercules Road, Sherford, Plymouth, PL9 8FA
        if rec["internal_council_id"] == "11218":
            rec["location"] = Point(-4.051082, 50.367181, srid=4326)

        # South Brent Village Hall, Station Approach, South Brent, TQ10 9JL
        if rec["internal_council_id"] == "11467":
            rec["location"] = Point(-3.835664, 50.428691, srid=4326)

        return rec
