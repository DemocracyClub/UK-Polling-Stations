from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "COV"
    addresses_name = (
        "2024-06-20/2024-06-06T15:02:00.371617/Democracy_Club__20June2024.tsv"
    )
    stations_name = (
        "2024-06-20/2024-06-06T15:02:00.371617/Democracy_Club__20June2024.tsv"
    )
    elections = ["2024-06-20"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # suspect
            "CV6 3FU",
            "CV6 3FT",
        ]:
            return None

        return super().address_record_to_dict(record)
