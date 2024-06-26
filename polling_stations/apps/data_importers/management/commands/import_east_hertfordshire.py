from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EHE"
    addresses_name = (
        "2024-07-04/2024-05-29T15:56:56.225774/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-29T15:56:56.225774/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10034624304",  # JACOB NEURO CENTRE, HIGH WYCH ROAD, SAWBRIDGEWORTH
            "10094847645",  # 18 GROSVENOR WALK, HERTFORD
            "10033105209",  # BEECHCROFT, STANDON GREEN END, HIGH CROSS, WARE
            "200002751708",  # PARK HOUSE, THE DRIVE, SAWBRIDGEWORTH
        ]:
            return None

        if record.addressline6 in [
            # split
            "CM21 0HX",
            "SG9 9DW",
            "CM23 3QY",
            # look wrong
            "SG12 0XY",
            "CM23 2EG",
            "CM23 4SA",
            "SG14 1FU",
            "SG13 7BE",
            "SG13 7BF",
            "SG14 2PQ",
            "SG14 1FT",
            "CM23 4SB",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # more accurate point for: Albury Village Hall, The Bourne, Clapgate, Albury, SG11 2BP
        if record.polling_place_id == "5971":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(0.093994, 51.903481, srid=4326)
            return rec

        return super().station_record_to_dict(record)
