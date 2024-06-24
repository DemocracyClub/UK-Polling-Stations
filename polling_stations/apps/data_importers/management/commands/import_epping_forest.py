from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EPP"
    addresses_name = "2024-07-04/2024-06-26T13:59:04.521969/EPP_combined.tsv"
    stations_name = "2024-07-04/2024-06-26T13:59:04.521969/EPP_combined.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10012157511",  # WALLED GARDEN HOUSE, EPPING
            "10012157510",  # TIMBER LODGE, EPPING
            "100091477396",  # SCHOOL HOUSE, KING HAROLD SCHOOL, BROOMSTICK HALL ROAD, WALTHAM ABBEY
            "100091249452",  # SHONKS FARM, MILL STREET, HARLOW
            "100091251326",  # THE PANTILES, DUNMOW ROAD, FYFIELD, ONGAR
            "100091251152",  # THATCHED COTTAGE, BIRDS GREEN, WILLINGALE, ONGAR
            "10022857710",  # BLUNTS FARMHOUSE COOPERSALE LANE, THEYDON BOIS, EPPING
            "100091247388",  # BROOKSIDE, GRAVEL LANE, CHIGWELL
            "10022857825",  # CARAVAN 2 MOSS NURSERY SEDGE GREEN, ROYDON, HARLOW
            "200002755166",  # GARDEN COTTAGE, NURSERY ROAD, LOUGHTON
        ]:
            return None

        if record.addressline6 in [
            # splits
            "CM16 6JA",
            "CM16 7QR",
            # suspect
            "CM5 0HP",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)
        # Coord fix from council for: High Beach Village Hall, Avey Lane, High Beach, Loughton
        if rec["internal_council_id"] == "3596":
            rec["location"] = Point(0.02918, 51.66369, srid=4326)

        return rec
