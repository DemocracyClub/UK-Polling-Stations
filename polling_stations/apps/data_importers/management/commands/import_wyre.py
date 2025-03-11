from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WYR"
    addresses_name = (
        "2025-05-01/2025-03-11T12:33:48.183418/Democracy_Club__01May2025.CSV"
    )
    stations_name = (
        "2025-05-01/2025-03-11T12:33:48.183418/Democracy_Club__01May2025.CSV"
    )
    elections = ["2025-05-01"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10024171572",  # WELL WOOD VIEW, STATION LANE, SCORTON, PRESTON
                "10034083802",  # FIELDVIEW, PINFOLD LANE, SOWERBY, PRESTON
                "100012846911",  # THE MOUNT HOTEL THE ESPLANADE, FLEETWOOD
                "10003530610",  # THE OLD PRINT WORKS BRUNA HILL, BARNACRE
                "10024173046",  # FORWARD2ME, YORK HOUSE, MANOR PARK, GREEN LANE WEST, GARSTANG, PRESTON
                "10024168892",  # OAK HOUSE, CLEVELEY BANK LANE, FORTON, PRESTON
                "10095963049",  # BOWLAND LODGE BOWLAND LAKES LEISURE VILLAGE CLEVELEY BANK LANE, FORTON
                "10024168891",  # POPLAR HOUSE, CLEVELEY BANK LANE, FORTON, PRESTON
            ]
        ):
            return None

        if record.post_code in [
            # split
            "FY6 8AR",
            # looks wrong
            "FY6 7GH",
            "PR3 1TS",
            "FY6 7BH",
            "PR3 0DW",
        ]:
            return None

        return super().address_record_to_dict(record)
