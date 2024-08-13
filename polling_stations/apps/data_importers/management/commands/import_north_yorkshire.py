from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NYE"
    addresses_name = (
        "2024-07-04/2024-06-01T16:22:27.231258/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-01T16:22:27.231258/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "200001017730",  # WILLOW FARM, DONCASTER ROAD, TADCASTER
                "200001023825",  # WHITEMOOR GRANGE WHITEMOOR LANE, BARLBY
                "10012901300",  # FLAT A ALBANY HOUSE CROWN CRESCENT, SCARBOROUGH
                "10012901301",  # FLAT B ALBANY HOUSE CROWN CRESCENT, SCARBOROUGH
                "10012901436",  # GEASEA COTTAGE, SAWDON, SCARBOROUGH
                "10090175389",  # ANNEXE, GEASEA COTTAGE, SAWDON, SCARBOROUGH
                "10093034006",  # 38 PADDOCK WAY, GREEN HAMMERTON, YORK
                "10093034565",  # OAK HOUSE PENNY POT LANE TO CENTRAL HOUSE FARM, HAMPSTHWAITE
                "10090348554",  # MEADOW VIEW 11A, RAVENSWORTH, RICHMOND
            ]
        ):
            return None
        if record.addressline6 in [
            # split
            "LS24 9HH",
            "YO14 9EW",
            "YO8 8JW",
            "HG5 8BD",
            "DL10 5JW",
            "YO12 5DB",
            "DL8 4AS",
            "DL10 4NP",
            "YO13 9PT",
            "HG3 3EG",
            "YO62 6JA",
            "DL9 4JA",
            "DL9 3JX",
            "DL2 2PW",
            "DL10 7PY",
            "YO17 9RL",
            "HG3 1FJ",
            "HG4 3LB",
            "DL8 4DY",
            "YO60 6PF",
            "YO62 6PE",
            "YO61 3GT",
            "YO61 4BW",
            "YO62 6PA",
            "DL11 6NT",
            "YO41 1JF",
            "HG5 0SB",
            "DL11 6PE",
            "HG3 1LT",
            "HG5 0FT",
            # suspect
            "DL10 5EY",
            "DL8 3DF",
        ]:
            return None
        return super().address_record_to_dict(record)
