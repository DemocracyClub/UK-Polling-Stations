from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TEW"
    addresses_name = (
        "2024-07-04/2024-06-03T20:51:01.069750/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-03T20:51:01.069750/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    # Checked and no correction needed:
    # WARNING: Polling station The Edge Community Centre (10642) is in Stroud District Council (STO)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "GL3 4ZR",
        ]:
            return None

        return super().address_record_to_dict(record)
