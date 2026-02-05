from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SAL"
    addresses_name = (
        "2026-05-07/2026-02-05T11:48:46.758061/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-05T11:48:46.758061/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200003633693",  # WOOD END, HATCHING GREEN, HARPENDEN
        ]:
            return None

        if record.addressline6 in [
            # splits
            "AL4 0LD",
            "AL1 3NS",
            "AL3 5PR",
            "AL3 5PD",
            # suspect
            "AL1 5NT",
        ]:
            return None

        return super().address_record_to_dict(record)
