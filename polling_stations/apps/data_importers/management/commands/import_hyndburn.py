from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HYN"
    addresses_name = (
        "2026-05-07/2026-03-05T10:21:19.955514/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-05T10:21:19.955514/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "100012393501",  # WELLSPRINGS FARM, SHAWCLIFFE LANE, GREAT HARWOOD, BLACKBURN, BB6 7UT
                "10009973780",  # RODGER HEY FARM, WHALLEY ROAD, GREAT HARWOOD, BLACKBURN, BB6 7UH
                "100012878207",  # LEG LOCK FARM, SOUGH LANE, GUIDE, BLACKBURN
                "10070894822",  # 2A HIGH STREET, RISHTON, BLACKBURN
                "10070894668",  # HARWOOD EDGE BARN, WILPSHIRE ROAD, RISHTON, BLACKBURN
                "100012393578",  # HARWOOD EDGE FARM, WILPSHIRE ROAD, RISHTON, BLACKBURN
            ]
        ):
            return None

        if record.addressline6 in [
            # split
            "BB5 5QA",
        ]:
            return None

        return super().address_record_to_dict(record)
