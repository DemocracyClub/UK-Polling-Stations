from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SHA"
    addresses_name = "2024-07-04/2024-06-14T11:36:22.227078/SHA_combined.tsv"
    stations_name = "2024-07-04/2024-06-14T11:36:22.227078/SHA_combined.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10008857241",  # GYPSY LANE SITE, BUCKFASTLEIGH
            "10008919040",  # LUDD FARM, UGBOROUGH, IVYBRIDGE
            "10008919308",  # THORNBROOK, THURLESTONE SANDS, KINGSBRIDGE
            "100040274671",  # BRITANNIA HOUSE, COLLEGE WAY, DARTMOUTH
            "10008912570",  # WILLANDS, MODBURY, IVYBRIDGE
            "10004745573",  # WATERSMEET, LUCAS WOOD, CORNWOOD, IVYBRIDGE
            "10008914019",  # THE SHIPPEN, SHERFORD, KINGSBRIDGE
            "10004748747",  # QUACK COTTAGE, DARTMOUTH
            "10008916701",  # WOODSIDE, BLACKPOOL, DARTMOUTH
            "100040298039",  # WELLS HOUSE, BARRACKS HILL, TOTNES
            "100040298047",  # WINDHOVER, BARRACKS HILL, TOTNES
            "100040282248",  # 33 ST. JOHNS ROAD, IVYBRIDGE
            "100040282247",  # 32 ST, JOHNS ROAD, IVYBRIDGE
            "10008909387",  # KEATON HOUSE, ERMINGTON, IVYBRIDGE
            "10008912790",  # HUNTERSFIELD, BLACKAWTON, TOTNES
            "10008912788",  # DUNKIRK HOUSE, BLACKAWTON, TOTNES
            "10009311941",  # THE ANNEXE SIDBORO HOUSE ROAD FROM OLDSTONE CROSS TO HEMBOROUGH POST, BLACKAWTON
            "10008918567",  # CALIFORNIA INN, MODBURY, IVYBRIDGE
            "10008912490",  # CALIFORNIA FARM, MODBURY, IVYBRIDGE
        ]:
            return None

        if record.addressline6 in [
            # looks wrong
            "TQ7 4DE",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # more accurate point for: South Brent Village Hall, Station Approach, South Brent, TQ10 9JL
        if rec["internal_council_id"] == "13005":
            rec["location"] = Point(-3.835664, 50.428691, srid=4326)

        # more accurate point for: Sherford Community Hub, Hercules Road, Sherford, Plymouth, PL9 8FA
        if rec["internal_council_id"] == "13175":
            rec["location"] = Point(-4.051082, 50.367181, srid=4326)

        return rec
