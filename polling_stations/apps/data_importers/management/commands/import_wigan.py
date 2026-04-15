from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WGN"
    addresses_name = (
        "2026-05-07/2026-04-15T11:55:41.446254/Democracy_Club__07May2026.CSV"
    )
    stations_name = (
        "2026-05-07/2026-04-15T11:55:41.446254/Democracy_Club__07May2026.CSV"
    )
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200002861926",  # THE COTTAGE, SANDY LANE, HINDLEY, WIGAN
            "100012500668",  # DODHURST BROW FARM, SANDY LANE, HINDLEY, WIGAN
            "100011823007",  # 165 WIGAN ROAD, ASHTON-IN-MAKERFIELD, WIGAN
            "10095424360",  # 109 ANCHOR FIELD, LEIGH
            "10095424324",  # 73 ANCHOR FIELD, LEIGH
            "10096704515",  # 5 LILY BANK MEADOW, LEIGH
        ]:
            return None

        if record.post_code in [
            # splits
            "WN7 4TF",
            "WN7 2LS",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # remove wrong coords for: St Aidans Parish Centre, Highfield Grange Ave, Winstanley, Wigan, WN3 6EE
        if record.polling_place_id == "12916":
            record = record._replace(
                polling_place_easting="0", polling_place_northing="0"
            )

        return super().station_record_to_dict(record)
