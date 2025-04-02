from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BNH"
    addresses_name = (
        "2025-05-01/2025-04-02T16:19:44.317384/Democracy_Club__01May2025 (9).tsv"
    )
    stations_name = (
        "2025-05-01/2025-04-02T16:19:44.317384/Democracy_Club__01May2025 (9).tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "22272586",  # 1 GREEN MEWS, 53 HOGARTH ROAD, HOVE
            "22272587",  # 2 GREEN MEWS, 53 HOGARTH ROAD, HOVE
            "22272588",  # 3 GREEN MEWS, 53 HOGARTH ROAD, HOVE
            "22279648",  # 184C PORTLAND ROAD, HOVE
        ]:
            return None

        return super().address_record_to_dict(record)
