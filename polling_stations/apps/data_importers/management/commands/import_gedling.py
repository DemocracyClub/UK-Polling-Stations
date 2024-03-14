from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "GED"
    addresses_name = (
        "2024-05-02/2024-03-14T10:08:50.224512/Democracy_Club__02May2024 (18).tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-14T10:08:50.224512/Democracy_Club__02May2024 (18).tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200004046660",  # COCKLIFFE COUNTRY HOUSE HOTEL, BURNTSTUMP HILL, ARNOLD, NOTTINGHAM
            "100032118065",  # 848A WOODBOROUGH ROAD, NOTTINGHAM
            "100031353751",  # 850 WOODBOROUGH ROAD, NOTTINGHAM
            "100031372068",  # THE FLAT TRAVELLERS REST MAPPERLEY PLAINS, LAMBLEY
            "100031372065",  # 10A BLENHEIM AVENUE, NOTTINGHAM
            "100032117629",  # THE FLAT WOODLARK INN CHURCH STREET, LAMBLEY
            "200002776955",  # 326 CARLTON HILL, CARLTON, NOTTINGHAM
            "10035282319",  # PENRHYN, MILL LANE, LAMBLEY, NOTTINGHAM
            "10035286332",  # 4 MILL LANE, LAMBLEY, NOTTINGHAM
            "100032276589",  # 163 STANDHILL ROAD, CARLTON, NOTTINGHAM
            "100032123942",  # 127 SPRING LANE, LAMBLEY, NOTTINGHAM
            "100031349971",  # E W WOOD BUILDERS, MANSFIELD HOUSE, 148 BURTON ROAD, GEDLING, NOTTINGHAM
            "100031349428",  # BROOKWOOD INSTALATIONS, 8A BROOKWOOD CRESCENT, CARLTON, NOTTINGHAM
            "100031350956",  # 216 CARLTON HILL, CARLTON, NOTTINGHAM
            "100031363324",  # 3 HASTINGS STREET, CARLTON, NOTTINGHAM
            "100031363326",  # 5 HASTINGS STREET, CARLTON, NOTTINGHAM
            "10035282383",  # 34 SUNRISE AVENUE, KILLARNEY PARK, NOTTINGHAM
            "100032276572",  # RESPECT FOR ANIMALS, 30 STATION ROAD, CARLTON, NOTTINGHAM
            "100031382797",  # FLAT 26-28 STATION ROAD, CARLTON
            "10035286081",  # 351B WESTDALE LANE, MAPPERLEY, NOTTINGHAM
            "200001152414",  # 361 WESTDALE LANE, MAPPERLEY, NOTTINGHAM
            "200001152416",  # 363 WESTDALE LANE, MAPPERLEY, NOTTINGHAM
            "10002888131",  # WESTDALE PHARMACY, 354 WESTDALE LANE, MAPPERLEY, NOTTINGHAM
            "100031382749",  # 38A STATION ROAD, CARLTON, NOTTINGHAM
            "100032126239",  # LEVERTONS, LODGE FARM, LIME LANE, ARNOLD, NOTTINGHAM
            "100032126019",  # FOREST FARM, MANSFIELD ROAD, ARNOLD, NOTTINGHAM
        ]:
            return None

        if record.addressline6 in [
            # splits
            "NG4 4FN",
            "NG3 6BN",
            "NG5 8AU",
            "NG4 2DX",
            "NG5 8AH",
            # looks wrong
            "NG14 6TN",
            "NG14 6RU",
        ]:
            return None

        return super().address_record_to_dict(record)
