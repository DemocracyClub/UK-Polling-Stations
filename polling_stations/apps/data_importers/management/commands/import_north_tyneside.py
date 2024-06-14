from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NTY"
    addresses_name = "2024-07-04/2024-06-14T14:09:24.864672/North Tyneside Council.tsv"
    stations_name = "2024-07-04/2024-06-14T14:09:24.864672/North Tyneside Council.tsv"
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "47243589",  # 14 BEECH WAY, KILLINGWORTH
            "47070238",  # EAST WIDEOPEN FARM COTTAGE, WIDEOPEN, NEWCASTLE UPON TYNE
            "47241411",  # OAK HOUSE, WIDEOPEN, NEWCASTLE UPON TYNE
            "47072178",  # FLAT ABOVE THE FOXHUNTERS PUBLIC HOUSE PRESTON NORTH ROAD, NORTH SHIELDS
            "47072124",  # CRICKET CLUB COTTAGE, PRESTON AVENUE, NORTH SHIELDS
            "47014289",  # FLAT ABOVE LOW LIGHTS TAVERN BREWHOUSE BANK, NORTH SHIELDS
            "47049172",  # 83 HOWDON ROAD, NORTH SHIELDS
            "47049170",  # 81 HOWDON ROAD, NORTH SHIELDS
            "47049168",  # 79 HOWDON ROAD, NORTH SHIELDS
            "47084844",  # FLAT ABOVE STATION HOTEL STATION ROAD, KILLINGWORTH
            "47229242",  # REDESDALE COURT, RAKE LANE, NORTH SHIELDS
            "47072123",  # PERCY PARK BUNGALOW, PRESTON AVENUE, NORTH SHIELDS
        ]:
            return None

        if record.addressline6 in [
            # splits
            "NE28 9GF",
            "NE12 8EE",
            # looks wrong
            "NE26 1LX",
            "NE28 9UR",
            "NE28 9UT",
            "NE13 6EN",
            "NE30 2ET",
        ]:
            return None

        return super().address_record_to_dict(record)
