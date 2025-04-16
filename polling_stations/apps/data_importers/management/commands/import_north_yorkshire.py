from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NYE"
    addresses_name = (
        "2025-05-01/2025-04-03T14:07:34.362862/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-04-03T14:07:34.362862/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
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
            "YO12 5DB",
        ]:
            return None
        return super().address_record_to_dict(record)
