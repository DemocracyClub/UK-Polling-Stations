from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOX"
    addresses_name = (
        "2025-05-01/2025-03-18T14:40:33.046028/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-18T14:40:33.046028/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10093354712",  # CROFTERS BARN, HIRONS HILL, LITTLE ROLLRIGHT, CHIPPING NORTON
                "10033224093",  # BREW HOUSE COTTAGE CHASTLETON HOUSE ROAD THROUGH CHASTLETON, CHASTLETON
                "10093354541",  # BARN CONVERSION BLISS FARM CHURCHILL ROAD, CHIPPING NORTON
                "10093355282",  # BOULTERS GRANGE, CHURCHILL ROAD, CHIPPING NORTON
                "10024177121",  # 1 TIMBER YARD, BRADWELL GROVE, BURFORD
                "10024177122",  # 2 TIMBER YARD, BRADWELL GROVE, BURFORD
                "10024177123",  # 3 TIMBER YARD, BRADWELL GROVE, BURFORD
                "10093356610",  # ANNEXE AT COLDSTONE HOUSE 50 SHIPTON ROAD, ASCOTT UNDER WYCHWOOD
                "100120969301",  # MANOR FARM, WESTCOTE BARTON, CHIPPING NORTON
                "100120968287",  # RICKYARD COTTAGE, FAIRGREEN, CHURCHILL, CHIPPING NORTON
                "10033227811",  # MANAGERS ACCOMMODATION CROSS KEYS 1 MARKET SQUARE, WITNEY
            ]
        ):
            return None

        if record.addressline6 in [
            # split
            "OX28 6DH",
            "OX18 1PU",
            "OX20 1RZ",
            "OX7 5YE",
            "OX7 4BJ",
            # suspect
            "OX7 6UQ",
            "OX7 6WJ",
            "OX7 6HX",
            "OX18 2BE",
        ]:
            return None

        return super().address_record_to_dict(record)
