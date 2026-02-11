from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MOL"
    addresses_name = (
        "2026-05-07/2026-02-11T14:42:39.273848/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-11T14:42:39.273848/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200000162928",  # 2 BLACKBROOK FARM COTTAGES, BLACKBROOK ROAD, DORKING
            "200000162927",  # 1 BLACKBROOK FARM COTTAGES, BLACKBROOK ROAD, DORKING
            "10000828494",  # ARNWOOD FARM COTTAGE RUSPER ROAD, NEWDIGATE
        ]:
            return None

        if record.addressline6 in [
            # splits
            "KT21 2LY",
        ]:
            return None

        return super().address_record_to_dict(record)
