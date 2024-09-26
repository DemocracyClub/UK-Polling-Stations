from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HYN"
    addresses_name = (
        "2024-07-04/2024-06-14T15:12:16.881791/Democracy_Club__04July2024 (30).tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-14T15:12:16.881791/Democracy_Club__04July2024 (30).tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10009967792",  # 3 HIGH STREET, ACCRINGTON
                "100012878207",  # LEG LOCK FARM, SOUGH LANE, GUIDE, BLACKBURN
                "10070894822",  # 2A HIGH STREET, RISHTON, BLACKBURN
                "10070896603",  # THE OLD STABLES BROWNSILLS, MILL LANE, GREAT HARWOOD, BLACKBURN
                "100012393501",  # WELLSPRINGS FARM, SHAWCLIFFE LANE, GREAT HARWOOD, BLACKBURN
                "100012393502",  # WYNGATE, SHAWCLIFFE LANE, GREAT HARWOOD, BLACKBURN
                "100012545092",  # CARPET PLANET & BEDS LTD, 55-57 WHALLEY ROAD, ACCRINGTON
                "10070894060",  # 2A WATER STREET, ACCRINGTON
                "10009969364",  # 2A LEMONIUS STREET, ACCRINGTON
                "100012392450",  # BUMPER HALL FARM, HASLINGDEN OLD ROAD, OSWALDTWISTLE, ACCRINGTON
                "10070895687",  # SQUIRREL BARN, GREEN HAWORTH, ACCRINGTON
                "10010696899",  # DUNSCAR FARM COTTAGE, WILPSHIRE ROAD, RISHTON, BLACKBURN
            ]
        ):
            return None

        if record.addressline6 in [
            # split
            "BB5 5QA",
            # suspect
            "BB5 6PW",
        ]:
            return None

        return super().address_record_to_dict(record)
