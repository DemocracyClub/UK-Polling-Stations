from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHW"
    addresses_name = (
        "2024-05-02/2024-04-08T13:57:14.878521/Democracy_Club__02May2024.CSV"
    )
    stations_name = (
        "2024-05-02/2024-04-08T13:57:14.878521/Democracy_Club__02May2024.CSV"
    )
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200003238923",  # THE OLD BARN, BRADSHAW BROOK FARM, MIDDLEWICH ROAD, ALLOSTOCK, KNUTSFORD
            "10091137623",  # 70 MUSKETT DRIVE, NORTHWICH
            "10091137622",  # 72 MUSKETT DRIVE, NORTHWICH
            "10091137631",  # 68 MUSKETT DRIVE, NORTHWICH
            "200002842851",  # GREVILLE HOUSE, GREVILLE DRIVE, WINSFORD
            "200000831359",  # OAK BANK, PARKGATE ROAD, CHESTER
            "200000990849",  # KIDNAL HOUSE, KIDNAL, MALPAS
            "100012360649",  # 6 LEIGHTON COTTAGES, BOATHOUSE LANE, PARKGATE, NESTON
            "10095485945",  # WESTVIEW, WELSH ROAD, LEDSHAM, ELLESMERE PORT
            "10094685291",  # 6 BALISTER DRIVE, HARTFORD, NORTHWICH
        ]:
            return None

        if record.addressline6 in [
            # splits
            "CW9 6EL",
            "CW9 8XB",
            "CW9 7SQ",
            "CH66 1NZ",
            "CW9 8PU",
            "CW7 2GG",
            "CH64 3SG",
            "CW7 3EQ",
            "CH4 7DG",
            "CW8 4AB",
            "CW6 9EP",
            "CW9 7RX",
            "CW8 4QS",
            "CH65 9JU",
            "WA6 0JA",
            "WA6 6LN",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Lower Peover CE Primary School, The Cobbles, Lower Peover, Knutsford, Cheshire, WA16 9PZ
        # Fixing the warning, correction is cosmetic and safe
        if record.polling_place_id == "11682":
            record = record._replace(
                polling_place_easting="374254", polling_place_northing="374113"
            )

        return super().station_record_to_dict(record)
