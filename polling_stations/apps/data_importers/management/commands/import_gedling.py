from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "GED"
    addresses_name = (
        "2025-05-01/2025-03-10T10:49:30.103808/Democracy_Club__01May2025 (3).tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-10T10:49:30.103808/Democracy_Club__01May2025 (3).tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
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
                "100031349971",  # E W WOOD BUILDERS, MANSFIELD HOUSE, 148 BURTON ROAD, GEDLING, NOTTINGHAM
                "10035282383",  # 34 SUNRISE AVENUE, KILLARNEY PARK, NOTTINGHAM
                "100032276572",  # RESPECT FOR ANIMALS, 30 STATION ROAD, CARLTON, NOTTINGHAM
                "100031382797",  # FLAT 26-28 STATION ROAD, CARLTON
            ]
        ):
            return None

        if record.addressline6 in [
            # splits
            "NG5 8AU",
            "NG4 4FN",
            "NG5 8AH",
            "NG3 6BN",
            "NG4 2DX",
            # looks wrong
            "NG14 6RU",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Fix coords for: Weaverthorpe Scout H.Q, Weaverthorpe Road, Woodthorpe, NG5 4PT (bug report 760)
        if record.polling_place_id == "4989":
            record = record._replace(
                polling_place_easting="459329",
                polling_place_northing="344419",
            )

        return super().station_record_to_dict(record)
