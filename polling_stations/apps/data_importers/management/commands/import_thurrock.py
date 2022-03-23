from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "THR"
    addresses_name = (
        "2022-05-05/2022-03-23T16:02:05.092550/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-23T16:02:05.092550/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):

        if record.addressline6.strip() in [
            "RM16 4RB",
            "RM19 1QJ",
        ]:
            return None  # split

        return super().address_record_to_dict(record)
