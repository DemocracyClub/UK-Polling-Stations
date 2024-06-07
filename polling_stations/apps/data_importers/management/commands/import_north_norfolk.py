from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NNO"
    addresses_name = (
        "2024-07-04/2024-06-07T11:53:17.956702/Democracy_Club__04July2024.CSV"
    )
    stations_name = (
        "2024-07-04/2024-06-07T11:53:17.956702/Democracy_Club__04July2024.CSV"
    )
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10034791449",  # THE CEDARS, GRESHAM, NORWICH
            "10023665747",  # CHALET 4 MILL FARM AYLSHAM ROAD, FELMINGHAM
            "10034812867",  # BURROW COTTAGE AT WARREN BARN BREWERY ROAD, TRUNCH
            "10034807115",  # 6 SEAWARD CREST, LINKS ROAD, MUNDESLEY, NORWICH
            "10034818211",  # GARDEN COTTAGE, HOVETON HALL ESTATE, HOVETON, NORWICH
            "10034793549",  # CLAPHAM DAMS FARM, TRIMINGHAM, NORWICH
            "10034815222",  # ANNEXE AT LANDGUARD HOUSE GIMINGHAM ROAD, TRIMINGHAM
            "10034793549",  # CLAPHAM DAMS FARM, TRIMINGHAM, NORWICH
            "100091558184",  # BELMONT HOUSE, CADOGAN ROAD, CROMER
            "10094471243",  # THE GRANARY, SLOLEY ROAD, SLOLEY, NORWICH
            "10094470883",  # THE OLD WORKSHOP, SLOLEY ROAD, SLOLEY, NORWICH
            "10034791501",  # BOUNDARY COTTAGE, GRUB STREET, HAPPISBURGH, NORWICH
            "10023457014",  # MALLARD RIVERSIDE ROAD, HOVETON
        ]:
            return None

        if record.addressline6 in [
            "NR11 7PE",  # splits
            "NR28 9NG",  # HAPPISBURGH ROAD, WHITE HORSE COMMON, NORTH WALSHAM
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Walcott Village Hall, Coast Road, Walcott, NR12 ONG
        # Misspell postcode, capital letter "O" should be a number "0"
        if record.polling_place_id == "21665":
            record = record._replace(polling_place_postcode="NR12 0NG")

        # St Benet Hall, St Nicholas Church Halls Complex, Vicarage Street, North Walsham, NR28 9BQ
        if record.polling_place_id == "21925":
            record = record._replace(polling_place_postcode="NR28 9BT")

        rec = super().station_record_to_dict(record)

        # Walsingham Parish Hall, 14 High Street, Walsingham, NR22 6AA
        if rec["internal_council_id"] == "22086":
            rec["location"] = Point(0.873339, 52.892674, srid=4326)

        return rec
