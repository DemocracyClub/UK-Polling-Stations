from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "GED"
    addresses_name = "2021-03-15T11:19:52.370890/Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-15T11:19:52.370890/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
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
            "100032123022",  # DAISIES DAY NURSERY, WOOD LANE, GEDLING, NOTTINGHAM
        ]:
            return None

        if record.addressline6 in [
            "NG5 8PJ",
            "NG4 1EN",
            "NG4 3DF",
            "NG14 6FN",
            "NG4 2DX",
            "NG4 3FT",
            "NG4 3GQ",
            "NG5 8AU",
            "NG4 3DH",
            "NG15 0BD",
            "NG15 8GD",
            "NG3 6HE",
            "NG3 6BN",
            "NG4 3DY",
        ]:
            return None

        return super().address_record_to_dict(record)
