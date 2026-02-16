from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NET"
    addresses_name = (
        "2026-05-07/2026-02-16T09:54:00.432797/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-16T09:54:00.432797/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "4510759485",  # FLAT PTE SOCIAL CLUB MILLERS ROAD, WALKER, NEWCASTLE UPON TYNE, NE6 2XP
                "4510015093",  # NORTH LODGE, JESMOND DENE ROAD, NEWCASTLE UPON TYNE, NE2 2EY
                "4510034357",  # LOUGH BRIDGE HOUSE, CALLERTON, NEWCASTLE UPON TYNE
                "4510044349",  # 11 ROKEBY AVENUE, NEWCASTLE UPON TYNE
                "4510044350",  # 12 ROKEBY AVENUE, NEWCASTLE UPON TYNE
                "4510014924",  # 34 DENTON AVENUE, NEWCASTLE UPON TYNE
                "4510083769",  # 278 FOSSWAY, NEWCASTLE UPON TYNE
                "4510141284",  # P T E SOCIAL CLUB, MILLERS ROAD, NEWCASTLE UPON TYNE
                "4510068272",  # 4 FAIRHOLM ROAD, NEWCASTLE UPON TYNE
                "4510044741",  # 1 THE RIDGEWAY, KENTON, NEWCASTLE UPON TYNE
                "4510018255",  # 1 HEXHAM AVENUE, NEWCASTLE UPON TYNE
                "4510746160",  # 241 ARMSTRONG ROAD, NEWCASTLE UPON TYNE
            ]
        ):
            return None

        if record.addressline6 in [
            # splits
            "NE4 9NQ",
            "NE15 9GJ",
            "NE5 1QF",
            # suspect
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Council has asked us not to show polling station locations
        record = record._replace(
            polling_place_uprn="", polling_place_easting="", polling_place_northing=""
        )

        return super().station_record_to_dict(record)
