from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NET"
    addresses_name = "2023-05-04/2023-03-27T13:58:53.599234/Updated 27..03.23 Democracy_Club__04May2023.tsv"
    stations_name = "2023-05-04/2023-03-27T13:58:53.599234/Updated 27..03.23 Democracy_Club__04May2023.tsv"
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "4510034357",  # LOUGH BRIDGE HOUSE, CALLERTON, NEWCASTLE UPON TYNE
            "4510044349",  # 11 ROKEBY AVENUE, NEWCASTLE UPON TYNE
            "4510044350",  # 12 ROKEBY AVENUE, NEWCASTLE UPON TYNE
            "4510014924",  # 34 DENTON AVENUE, NEWCASTLE UPON TYNE
            "4510095971",  # 2 WOODSTOCK ROAD, NEWCASTLE UPON TYNE
            "4510048289",  # 56 WOODSTOCK ROAD, NEWCASTLE UPON TYNE
            "4510755893",  # 63 WHITE HOUSE ROAD, NEWCASTLE UPON TYNE
            "4510001747",  # 53 CAROLINE STREET, NEWCASTLE UPON TYNE
            "4510106463",  # 2 CLIFFORD ROAD, NEWCASTLE UPON TYNE
            "4510115273",  # 250 ST. ANTHONYS ROAD, NEWCASTLE UPON TYNE
            "4510755706",  # 633 WELBECK ROAD, NEWCASTLE UPON TYNE
            "4510083769",  # 278 FOSSWAY, NEWCASTLE UPON TYNE
            "4510116542",  # 515 SHIELDS ROAD, NEWCASTLE UPON TYNE
            "4510141284",  # P T E SOCIAL CLUB, MILLERS ROAD, NEWCASTLE UPON TYNE
            "4510759485",  # FLAT PTE SOCIAL CLUB MILLERS ROAD, NEWCASTLE UPON TYNE
            "4510759781",  # 135 FENHAM HALL DRIVE, NEWCASTLE UPON TYNE
            "4510092926",  # 15 SANDRINGHAM ROAD, GOSFORTH, NEWCASTLE UPON TYNE
            "4510041714",  # 11 SANDRINGHAM ROAD, GOSFORTH, NEWCASTLE UPON TYNE
            "4510041715",  # 13 SANDRINGHAM ROAD, GOSFORTH, NEWCASTLE UPON TYNE
            "4510116916",  # 5 STONEYHURST ROAD WEST, NEWCASTLE UPON TYNE
            "4510731041",  # FLAT, 6 ST. MARYS PLACE, NEWCASTLE UPON TYNE
            "4510728933",  # THE BUNGALOW EXHIBITION PARK CLAREMONT ROAD, NEWCASTLE UPON TYNE
        ]:
            return None

        if record.addressline6 in [
            # splits
            "NE4 9NQ",
            "NE5 1QF",
            "NE15 9FD",  # GOLDCREST ROAD, NEWCASTLE UPON TYNE
            "NE6 4AZ",  # HADRIANS DRIVE, NEWCASTLE UPON TYNE
            "NE5 2BR",  # SANDRINGHAM ROAD, EAST DENTON, NEWCASTLE UPON TYNE
            "NE7 7BQ",  # JESMOND DENE, NEWCASTLE UPON TYNE
        ]:
            return None  # split

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Following warning was checked and there is no need for changes:
        # WARNING: P'Civic Centre Grand Entrance' and 'Civic Centre Arches Reception' are at approximately
        # the same location, but have different postcodes: '12808','12805'

        rec = super().station_record_to_dict(record)

        # West End Library and Community Hub, Condercum Road, Newcastle upon Tyne, NE4 9JH
        if rec["internal_council_id"] == "12697":
            rec["location"] = Point(-1.660097, 54.971494, srid=4326)

        # Gosforth Parish Church Hall, Wardle Street, Off Church Avenue, Newcastle upon Tyne
        if rec["internal_council_id"] == "12650":
            rec["location"] = Point(-1.608869, 55.006395, srid=4326)

        return rec
