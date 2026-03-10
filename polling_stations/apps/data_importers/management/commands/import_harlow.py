from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAR"
    addresses_name = (
        "2026-05-07/2026-03-10T11:20:18.634645/Democracy_Club__07May2026.CSV"
    )
    stations_name = (
        "2026-05-07/2026-03-10T11:20:18.634645/Democracy_Club__07May2026.CSV"
    )
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100091255475",  # NEXUS HOUSE, SCHOOL LANE, HARLOW
        ]:
            return None

        if record.addressline6 in [
            # splits
            "CM20 1BA",
        ]:
            return None

        return super().address_record_to_dict(record)
