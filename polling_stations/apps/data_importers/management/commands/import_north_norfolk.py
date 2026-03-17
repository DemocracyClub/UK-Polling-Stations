from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NNO"
    addresses_name = (
        "2026-05-07/2026-03-17T09:14:33.369588/NNDC Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-17T09:14:33.369588/NNDC Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10094472705",  # THE DAIRY STODY HALL BRINTON ROAD, STODY, NR24 2ED
            "10034791449",  # THE CEDARS, GRESHAM, NORWICH
            "10023665747",  # CHALET 4 MILL FARM AYLSHAM ROAD, FELMINGHAM
            "10034812867",  # BURROW COTTAGE AT WARREN BARN BREWERY ROAD, TRUNCH
            "10034818211",  # GARDEN COTTAGE, HOVETON HALL ESTATE, HOVETON, NORWICH
            "10034793549",  # CLAPHAM DAMS FARM, TRIMINGHAM, NORWICH
            "10034815222",  # ANNEXE AT LANDGUARD HOUSE GIMINGHAM ROAD, TRIMINGHAM
            "10034793549",  # CLAPHAM DAMS FARM, TRIMINGHAM, NORWICH
            "100091558184",  # BELMONT HOUSE, CADOGAN ROAD, CROMER
            "10094471243",  # THE GRANARY, SLOLEY ROAD, SLOLEY, NORWICH
            "10094470883",  # THE OLD WORKSHOP, SLOLEY ROAD, SLOLEY, NORWICH
            "10034791501",  # BOUNDARY COTTAGE, GRUB STREET, HAPPISBURGH, NORWICH
        ]:
            return None

        if record.addressline6 in [
            # splits
            "NR11 7PE",
            # looks wrong
            "NR28 9NG",
            "NR11 7QE",
            "NR11 8RS",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Walcott Village Hall, Coast Road, Walcott, NR12 ONG
        # Misspell postcode, capital letter "O" should be a number "0"
        if record.polling_place_id == "26033":
            record = record._replace(polling_place_postcode="NR12 0NG")

        # St Benet Hall, St Nicholas Church Halls Complex, Vicarage Street, North Walsham, NR28 9BQ
        if record.polling_place_id == "26363":
            record = record._replace(polling_place_postcode="NR28 9BT")

        rec = super().station_record_to_dict(record)

        # Walsingham Parish Hall, 14 High Street, Walsingham, NR22 6AA
        if rec["internal_council_id"] == "26534":
            rec["location"] = Point(0.873339, 52.892674, srid=4326)

        return rec
