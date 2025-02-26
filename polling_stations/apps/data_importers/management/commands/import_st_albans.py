from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SAL"
    addresses_name = (
        "2025-05-01/2025-02-26T08:45:19.492509/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-02-26T08:45:19.492509/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200003633693",  # WOOD END, HATCHING GREEN, HARPENDEN
            "100081134635",  # PLAISTOWES FARM, NOKE LANE, ST. ALBANS
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
