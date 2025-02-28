from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WAW"
    addresses_name = (
        "2025-05-01/2025-02-28T09:36:47.805307/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-02-28T09:36:47.805307/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "100071258162",  # BUDBROOKE LODGE FARM, HAMPTON ROAD, WARWICK
                "100071258929",  # FLAT VINE INN 86-88 WEST STREET, WARWICK
                "10013184069",  # THE BUNGALOW, GUYS CLIFFE STABLES, GUYS CLIFFE, WARWICK
                "100071258712",  # FLAT 32 SPINNEY HILL, WARWICK
                "100071255338",  # 14B REGENCY HOUSE NEWBOLD TERRACE, LEAMINGTON SPA
                "10023406679",  # 44 WARWICK PLACE, LEAMINGTON SPA
                "10094931337",  # 28 SANDPIT BOULEVARD, WARWICK
                "10013183598",  # THE FLAT THE WATERSIDE INN QUEENSWAY, LEAMINGTON SPA
                "10003785246",  # QUAIL COTTAGE, CHASE LANE, KENILWORTH
                "10090527829",  # ASPS FARM, BANBURY ROAD, WARWICK	CV34 6SS
                "10013182829",  # HEATHCOTE HOUSE, HARBURY LANE, HEATHCOTE, WARWICK	CV34 6SL
            ]
        ):
            return None

        if record.addressline6 in [
            # split
            "CV32 5TA",
            "CV32 7AW",
            "CV34 5BY",
            "CV8 2FE",
            "CV31 1BN",
            "CV32 6AN",
            # suspect
            "CV34 8BP",  # UPPERFIELD ROAD, WARWICK
            "CV8 1DX",  # OAKS FARM, FARM ROAD
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Temporary Building, (Grassed area), Fusiliers Way, Warwick
        if record.polling_place_id == "14926":
            record = record._replace(polling_place_postcode="CV34 8AG")

        return super().station_record_to_dict(record)
