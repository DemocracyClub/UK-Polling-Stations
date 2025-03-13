from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CAT"
    addresses_name = (
        "2025-05-01/2025-03-13T14:43:22.853120/Democracy_Club__01May2025.CSV"
    )
    stations_name = (
        "2025-05-01/2025-03-13T14:43:22.853120/Democracy_Club__01May2025.CSV"
    )
    elections = ["2025-05-01"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10094583530",  # SHIRE COTTAGE, FORD, HOATH, CANTERBURY
        ]:
            return None

        return super().address_record_to_dict(record)
