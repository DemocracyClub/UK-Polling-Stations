from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SGC"
    addresses_name = (
        "2024-02-15/2024-01-30T11:10:09.091156/Democracy_Club__15February2024.tsv"
    )
    stations_name = (
        "2024-02-15/2024-01-30T11:10:09.091156/Democracy_Club__15February2024.tsv"
    )
    elections = ["2024-02-15"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "BS15 3HW",
            "BS15 3HP",
            # suspect
            "BS30 6NR",
        ]:
            return None

        return super().address_record_to_dict(record)
