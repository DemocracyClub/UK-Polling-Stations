from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SGC"
    addresses_name = (
        "2023-05-04/2023-03-30T09:28:07.467090/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-30T09:28:07.467090/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "BS37 6DF",
            "BS37 7BZ",
            "BS16 4LZ",
            "BS15 3HP",
            "GL12 8HT",
            "BS15 3HW",
            "BS30 5TP",
            "BS32 4AH",
        ]:
            return None

        return super().address_record_to_dict(record)
