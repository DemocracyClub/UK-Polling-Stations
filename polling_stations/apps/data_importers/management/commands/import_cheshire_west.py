from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHW"
    addresses_name = (
        "2023-05-04/2023-04-14T11:06:40.402596/Democracy_Club__04May2023.CSV"
    )
    stations_name = (
        "2023-05-04/2023-04-14T11:06:40.402596/Democracy_Club__04May2023.CSV"
    )
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200003238923",  # THE OLD BARN, BRADSHAW BROOK FARM, MIDDLEWICH ROAD, ALLOSTOCK, KNUTSFORD
            "10091137623",  # 70 MUSKETT DRIVE, NORTHWICH
            "10091137622",  # 72 MUSKETT DRIVE, NORTHWICH
            "10091137631",  # 68 MUSKETT DRIVE, NORTHWICH
            "200002842851",  # GREVILLE HOUSE, GREVILLE DRIVE, WINSFORD
            "100012372274",  # STANTHORNE HALL FARM, MIDDLEWICH ROAD, STANTHORNE, MIDDLEWICH
            "100012353201",  # STREET FARM, KELSALL ROAD, TARVIN, CHESTER
            "200000831359",  # OAK BANK, PARKGATE ROAD, CHESTER
            "200000832902",  # LOWCROSS MILL, LOWCROSS, TILSTON, MALPAS
            "200000990850",  # KIDNAL COTTAGE, KIDNAL, MALPAS
        ]:
            return None

        if record.addressline6 in [
            # splits
            "CW7 3EQ",
            "CW9 8PU",
            "CH66 1NZ",
            "CW9 6EL",
            "CW9 8XB",
            "CH65 9JU",
            "CW8 4AB",
            "CW7 2GG",
            "CW9 7RX",
            "CH64 3SG",
            "CW8 2NQ",
            "CW6 9EP",
            "WA6 0JA",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # The Upton Royal British Legion, 20 Heath Road, Upton, Chester, CH1 1HX
        # Proposed postcode correction: CH2 1HX
        if record.polling_place_id == "9689":
            record = record._replace(polling_place_postcode="")

        # Mobile Polling Station - Cheviot Square, Cheviot Square, Winsford
        # Proposed postcode correction: CW7 1QS
        if record.polling_place_id == "9643":
            record = record._replace(polling_place_postcode="")

        # Lower Peover CE Primary School, The Cobbles, Lower Peover, Knutsford, Cheshire, WA16 9PZ
        # Fixing the warning, correction is cosmetic and safe
        if record.polling_place_id == "9447":
            record = record._replace(
                polling_place_easting="374254", polling_place_northing="374113"
            )

        return super().station_record_to_dict(record)
