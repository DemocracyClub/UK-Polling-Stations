from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BUR"
    addresses_name = (
        "2026-04-02/2026-03-04T17:11:34.630288/Democracy_Club__02April2026.tsv"
    )
    stations_name = (
        "2026-04-02/2026-03-04T17:11:34.630288/Democracy_Club__02April2026.tsv"
    )
    elections = ["2026-04-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # suspect
            "BL8 1TF",
        ]:
            return None

        return super().address_record_to_dict(record)
