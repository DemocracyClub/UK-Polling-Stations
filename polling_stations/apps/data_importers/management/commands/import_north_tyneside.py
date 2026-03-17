from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NTY"
    addresses_name = (
        "2026-05-07/2026-03-17T14:43:43.621138/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-17T14:43:43.621138/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "47247521",  # 1 UPPER CAMDEN STREET, NORTH SHIELDS, NE30 1QG
                "47001096",  # 7A ALBION ROAD, NORTH SHIELDS, NE30 2RJ
                "47000579",  # FLAT ABOVE THE JOLLY BOWMAN ADDINGTON DRIVE, HADRIAN PARK, WALLSEND, NE28 9UR
                "47070238",  # EAST WIDEOPEN FARM COTTAGE, WIDEOPEN, NEWCASTLE UPON TYNE, NE13 6DW
                "47084844",  # FLAT ABOVE STATION HOTEL STATION ROAD, KILLINGWORTH, NE12 6RA
                "47243589",  # 14 BEECH COURT, CAMPERDOWN, NEWCASTLE UPON TYNE, NE12 5AE
                "47243589",  # 14 BEECH WAY, KILLINGWORTH
                "47070238",  # EAST WIDEOPEN FARM COTTAGE, WIDEOPEN, NEWCASTLE UPON TYNE
                "47014289",  # FLAT ABOVE LOW LIGHTS TAVERN BREWHOUSE BANK, NORTH SHIELDS
                "47229242",  # REDESDALE COURT, RAKE LANE, NORTH SHIELDS
            ]
        ):
            return None

        if record.addressline6 in [
            # splits
            "NE28 8BQ",
            "NE29 8RR",
            # suspect
            "NE28 8AQ",
            "NE28 8BN",
            "NE12 6AA",
            "NE13 6EN",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # waiting for council response
        # postcode correction for: Temporary Polling Station - QB, Junction of Upper Elsdon Street and Seymour Street, North Shields
        # if record.polling_place_id == "4087":
        #     record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)
