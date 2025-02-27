from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHA"
    addresses_name = "2025-05-01/2025-02-27T11:03:15.607692/Democracy_Club__01May2025 (27-02-2025).tsv"
    stations_name = "2025-05-01/2025-02-27T11:03:15.607692/Democracy_Club__01May2025 (27-02-2025).tsv"
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        if (
            uprn
            in [
                "10091071561",  # THE OLD FARM HOUSE, SCHOOL LANE, BIRSTALL, LEICESTER
                "100030446529",  # 70 HIGH STREET, BARROW UPON SOAR, LOUGHBOROUGH
                "100032039889",  # 27 MARKET PLACE, LOUGHBOROUGH
                "100030447889",  # ROECLIFFE FARM, JOE MOORES LANE, WOODHOUSE EAVES, LOUGHBOROUGH
                "100030433587",  # MUCKLIN LODGE, MAIN STREET, WOODTHORPE, LOUGHBOROUGH
                "100032069971",  # 383 FOSSE WAY, RATCLIFFE ON THE WREAKE, LEICESTER
                "100030416263",  # 381 FOSSE WAY, RATCLIFFE ON THE WREAKE, LEICESTER
                "100030438667",  # 76 CHAVENEY ROAD, QUORN, LOUGHBOROUGH
            ]
        ):
            return None

        if record.addressline6 in [
            # splits
            "LE11 5JQ",
            # suspect
            "LE7 7GA",  # BRADGATE ROAD, CROPSTON, LEICESTER
            "LE11 5FJ",  # COTTON WAY, LOUGHBOROUGH
            "LE12 7SF",  # HOBBS WICK, SILEBY, LOUGHBOROUGH
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Investigated and ignored the following warning:
        # WARNING: Polling station St Margarets Co-Operative Club (13041) is in Leicester City Council (LCE)
        # but target council is Charnwood Borough Council (CHA) - manual check recommended

        return super().station_record_to_dict(record)
