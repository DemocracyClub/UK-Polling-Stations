from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SWD"
    addresses_name = (
        "2026-05-07/2026-02-10T09:40:26.696932/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-10T09:40:26.696932/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10004842282",  # 15B VICTORIA ROAD, SWINDON
            "10004837805",  # 15A VICTORIA ROAD, SWINDON
            "200001616306",  # ANDY WRAIGHT TEACHING STUDIOS, 105 RODBOURNE ROAD, SWINDON
            "10004845458",  # FLAT 16 VICTORIA ROAD, OLD TOWN, SWINDON
            "200002920837",  # 597 CRICKLADE ROAD, SWINDON
            "100121168491",  # MILL STONE HOUSE, MILL LANE, SWINDON
        ]:
            return None

        if record.addressline6 in [
            # splits
            "SN6 7JY",
            "SN25 2TN",
            "SN25 3LR",
            # looks wrong
            "SN3 3GE",
        ]:
            return None

        return super().address_record_to_dict(record)
