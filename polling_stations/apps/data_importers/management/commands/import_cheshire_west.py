from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHW"
    addresses_name = (
        "2024-07-04/2024-06-18T10:00:13.527644/Democracy_Club__04July2024 (31).tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-18T10:00:13.527644/Democracy_Club__04July2024 (31).tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10091137623",  # 70 MUSKETT DRIVE, NORTHWICH
            "10091137622",  # 72 MUSKETT DRIVE, NORTHWICH
            "10091137631",  # 68 MUSKETT DRIVE, NORTHWICH
            "200002842851",  # GREVILLE HOUSE, GREVILLE DRIVE, WINSFORD
            "200000831359",  # OAK BANK, PARKGATE ROAD, CHESTER
            "200000990849",  # KIDNAL HOUSE, KIDNAL, MALPAS
            "100012360649",  # 6 LEIGHTON COTTAGES, BOATHOUSE LANE, PARKGATE, NESTON
            "10095485945",  # WESTVIEW, WELSH ROAD, LEDSHAM, ELLESMERE PORT
            "10094685291",  # 6 BALISTER DRIVE, HARTFORD, NORTHWICH
            "10093981388",  # 16 LANCASTER GARDENS, ELLESMERE PORT
            "10093486377",  # 89 THORNTON ROAD, ELLESMERE PORT
            "10093486380",  # 1 CINDER CLOSE, ELLESMERE PORT
            "10093486372",  # 2 VICTORY COURT, ELLESMERE PORT
            "200000832902",  # LOWCROSS MILL, LOWCROSS, TILSTON, MALPAS
        ]:
            return None

        if record.addressline6 in [
            # splits
            "CW9 8PU",
            "CW8 4BT",
            "CH4 7DG",
            "CH65 9JU",
            "CH64 3SG",
            "CW7 2GG",
            "CW7 3EQ",
            "CW8 4AB",
            "CH66 1NZ",
            "CW6 9EP",
        ]:
            return None

        return super().address_record_to_dict(record)
