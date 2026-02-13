from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HRY"
    addresses_name = (
        "2026-05-07/2026-02-13T11:56:45.695561/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-13T11:56:45.695561/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "100021201447",  # GROUND FLOOR RIGHT FLAT 12 METHUEN PARK, HORNSEY, LONDON
                "10022941817",  # FLAT C 121 BOUNDS GREEN ROAD, WOOD GREEN, LONDON
                "10093591148",  # FLAT 24 RIDDELL COURT PEMBROKE ROAD, HORNSEY, LONDON
                "100021162190",  # 4 CAMPSBOURNE ROAD, LONDON
                "100021162186",  # 2 CAMPSBOURNE ROAD, LONDON
                "10003983434",  # GROUND AND FIRST FLOOR LEFT FLAT 12 METHUEN PARK, HORNSEY, LONDON
                "100021195610",  # FLAT B 41 LANGHAM ROAD, TOTTENHAM, LONDON
                "100023152045",  # FLAT A 41 LANGHAM ROAD, TOTTENHAM, LONDON
                "100021197338",  # 9B LINDEN ROAD, LONDON
                "100021195611",  # FLAT C 41 LANGHAM ROAD, TOTTENHAM, LONDON
                "100021197337",  # 9A LINDEN ROAD, LONDON
                "100023152047",  # FLAT B 29 LANGHAM ROAD, TOTTENHAM, LONDON
                "100023152046",  # FLAT A 29 LANGHAM ROAD, TOTTENHAM, LONDON
                "10022939227",  # 398A WEST GREEN ROAD, LONDON
                "100021224745",  # 2 ST. ANN'S ROAD, LONDON
                "100021190559",  # 107 HIGH ROAD, LONDON
                "100021201445",  # FIRST FLOOR RIGHT FLAT 12 METHUEN PARK, HORNSEY, LONDON
                "100021215240",  # GROUND FLOOR FLAT B 1 PRIORY ROAD, HORNSEY, LONDON
                "100023165900",  # 861 HIGH ROAD, TOTTENHAM, LONDON
                "10022936455",  # FLAT B 489 SEVEN SISTERS ROAD, TOTTENHAM, LONDON
                "100021190559",  # 107 HIGH ROAD, LONDON
                "100021190663",  # SECOND FLOOR FLAT 31 HIGH STREET, HORNSEY, LONDON
                "10093590571",  # FLAT 1, 36 WILLOUGHBY ROAD, LONDON
                "10022942491",  # FLAT D1 10 HIGH ROAD, WOOD GREEN, LONDON
                "10022937525",  # FLAT 5, 32 COURCY ROAD, LONDON
                "100021192891",  # FLAT B 42 HORNSEY PARK ROAD, WOOD GREEN, LONDON
                "100021192893",  # FLAT A 42 HORNSEY PARK ROAD, WOOD GREEN, LONDON
            ]
        ):
            return None
        if record.addressline6 in [
            # split
            "N17 7AT",
            # looks wrong
            "N8 0FT",
            "N15 3RA",
            "N17 0JY",
        ]:
            return None

        return super().address_record_to_dict(record)
