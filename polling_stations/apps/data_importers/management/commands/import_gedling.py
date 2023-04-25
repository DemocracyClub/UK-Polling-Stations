from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "GED"
    addresses_name = (
        "2023-05-04/2023-04-21T14:14:24.161747/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-21T14:14:24.161747/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200004046660",  # COCKLIFFE COUNTRY HOUSE HOTEL, BURNTSTUMP HILL, ARNOLD, NOTTINGHAM
            "100032118065",  # 848A WOODBOROUGH ROAD, NOTTINGHAM
            "100031353751",  # 850 WOODBOROUGH ROAD, NOTTINGHAM
            "100031372068",  # THE FLAT TRAVELLERS REST MAPPERLEY PLAINS, LAMBLEY
            "100031372065",  # 10A BLENHEIM AVENUE, NOTTINGHAM
            "100032125606",  # THE FLAT FRIAR TUCK GEDLING ROAD, ARNOLD
            "100032117629",  # THE FLAT WOODLARK INN CHURCH STREET, LAMBLEY
            "200002776955",  # 326 CARLTON HILL, CARLTON, NOTTINGHAM
            "10035282319",  # PENRHYN, MILL LANE, LAMBLEY, NOTTINGHAM
            "10035286332",  # 4 MILL LANE, LAMBLEY, NOTTINGHAM
            "100032276589",  # 163 STANDHILL ROAD, CARLTON, NOTTINGHAM
            "100032302726",  # THE FLAT FOX AND HOUNDS HOTEL STATION ROAD, CARLTON
            "10035288244",  # 93 SPRING LANE, LAMBLEY
            "100032123942",  # 127 SPRING LANE, LAMBLEY, NOTTINGHAM
            "100031349971",  # E W WOOD BUILDERS, MANSFIELD HOUSE, 148 BURTON ROAD, GEDLING, NOTTINGHAM
            "100031345829",  # SCOTGRAVE FARM, ARNOLD LANE, GEDLING, NOTTINGHAM
        ]:
            return None

        if record.addressline6 in [
            # splits
            "NG5 8AH",
            "NG3 6BN",
            "NG4 2DX",
            "NG5 8AU",
            "NG4 4FN",
        ]:
            return None

        return super().address_record_to_dict(record)
