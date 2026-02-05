from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CRY"
    addresses_name = (
        "2026-05-07/2026-02-05T13:28:59.885856/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-05T13:28:59.885856/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100020676357",  # 18A CROHAM ROAD, SOUTH CROYDON
            "10093049200",  # 16 LIMPSFIELD ROAD, SOUTH CROYDON
            "10093049201",  # 16A LIMPSFIELD ROAD, SOUTH CROYDON
            "10093049201",  # 16A LIMPSFIELD ROAD, SOUTH CROYDON
            "200001221192",  # 141 BRIGHTON ROAD, PURLEY
            "10014054732",  # 97 NOVA ROAD, CROYDON
            "10014054731",  # 95 NOVA ROAD, CROYDON
            "10094493457",  # 44 COOMBE ROAD, CROYDON
            "100020690731",  # 39 BRICKFIELD ROAD, THORNTON HEATH
            "100020584917",  # WEST LODGE, BISHOPS WALK, CROYDON
        ]:
            return None

        if record.addressline6 in [
            # looks wrong
            "SE19 3FB",
            "CR8 3ES",
            "CR5 3NY",
            "CR3 5QQ",
            "CR2 0FP",
        ]:
            return None

        return super().address_record_to_dict(record)
