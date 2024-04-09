from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NYE"
    addresses_name = (
        "2024-05-02/2024-04-04T11:45:50.805143/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-04-04T11:45:50.805143/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # St Michaels & All Angels Church Hall - Scarborough, Filey Road, Scarborough, YO11 3JG
        if record.polling_place_id == "80279":
            record = record._replace(polling_place_postcode="YO11 3AA")
        # Low Row and Feetham Literary Institute, Low Row DL10 6NA
        if record.polling_place_id == "79859":
            record = record._replace(polling_place_postcode="DL11 6NA")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200001017730",  # WILLOW FARM, DONCASTER ROAD, TADCASTER
            "200001023825",  # WHITEMOOR GRANGE WHITEMOOR LANE, BARLBY
            "10012901300",  # FLAT A ALBANY HOUSE CROWN CRESCENT, SCARBOROUGH
            "10012901301",  # FLAT B ALBANY HOUSE CROWN CRESCENT, SCARBOROUGH
            "10012901436",  # GEASEA COTTAGE, SAWDON, SCARBOROUGH
            "10090175389",  # ANNEXE, GEASEA COTTAGE, SAWDON, SCARBOROUGH
            "10093034006",  # 38 PADDOCK WAY, GREEN HAMMERTON, YORK
            "10093034565",  # OAK HOUSE PENNY POT LANE TO CENTRAL HOUSE FARM, HAMPSTHWAITE
            "10090348554",  # MEADOW VIEW 11A, RAVENSWORTH, RICHMOND
        ]:
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
            # suspect
            "DL10 5EY" "DL8 3DF",
        ]:
            return None
        return super().address_record_to_dict(record)
