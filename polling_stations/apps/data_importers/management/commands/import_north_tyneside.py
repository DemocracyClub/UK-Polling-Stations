from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NTY"
    addresses_name = (
        "2024-05-02/2024-03-11T10:30:17.403600/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-11T10:30:17.403600/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
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

    def station_record_to_dict(self, record):
        # postcode correction for: Fernedene, Threap Gardens, Howdon, NE28 6SL
        if record.polling_place_id == "2825":
            record = record._replace(polling_place_postcode="NE28 7HT")

        return super().station_record_to_dict(record)
