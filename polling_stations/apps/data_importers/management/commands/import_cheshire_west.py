from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHW"
    addresses_name = "2021-04-16T11:58:13.470921/Cheshire West and Chester Democracy_Club__06May2021.tsv"
    stations_name = "2021-04-16T11:58:13.470921/Cheshire West and Chester Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        if record.polling_place_id in [
            "7372",  # Meadow Bank Social Club School Road Meadow Bank, Winsford CW7 9PG
            "7374",  # Darnhall Village Hall Hall Lane Darnhall, Winsford CW7 4D9
        ]:
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100012373488",  # THE OLD FARMHOUSE, HOUGH LANE, COMBERBACH, NORTHWICH
            "10091137631",  # 68 MUSKETT DRIVE, NORTHWICH
            "10091137623",  # 70 MUSKETT DRIVE, NORTHWICH
            "10091137622",  # 72 MUSKETT DRIVE, NORTHWICH
            "10093983974",  # OAKWOOD MARINA, DAVENHAM ROAD, BILLINGE GREEN, NORTHWICH
            "10091141908",  # MILL COTTAGE, STATION ROAD, CROWTON, NORTHWICH
            "200003227699",  # THE OLD STABLEHOUSE, DOBERS LANE, FRODSHAM
            "10091141075",  # SKY HOUSE, TIRLEY LANE, UTKINTON, TARPORLEY
            "100012360649",  # 6 LEIGHTON COTTAGES, BOATHOUSE LANE, PARKGATE, NESTON
            "100010033259",  # 45 WEALSTONE LANE, UPTON, CHESTER
            "10014510578",  # THE COACH HOUSE, PLATTS LANE, HATTON HEATH, CHESTER
            "10093485405",  # NEWTON FIELDS, OLDCASTLE LANE, CUDDINGTON, MALPAS
            "200000831359",  # OAK BANK, PARKGATE ROAD, CHESTER
        ]:
            return None

        if record.addressline6 in [
            "CH64 7TG",
            "CH64 3SG",
            "CH65 9JU",
            "WA6 0JA",
            "WA6 9EG",
            "CW8 4QS",
            "CW8 2NQ",
            "CW7 2HL",
            "CW9 8PU",
            "CW7 2PU",
            "CW6 0JQ",
            "CW6 9EP",
            "CW7 3EQ",
            "CW7 2GG",
            "CW9 6EL",
            "CW9 7RL",
            "CW9 7RX",
            "WA6 7EP",
            "WA6 7HQ",
            "CW9 8XB",
            "CW8 4AB",
            "CW8 4YP",
        ]:
            return None

        return super().address_record_to_dict(record)
