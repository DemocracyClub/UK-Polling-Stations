from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BUR"
    addresses_name = (
        "2022-05-05/2022-03-24T12:31:09.109523/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-24T12:31:09.109523/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "BL9 8HB",
            "BL9 9JW",
            "BL9 8JJ",
            "BL9 8JW",
            "BL9 9PQ",
            "BL8 2HH",
            "BL8 1TF",
        ]:
            return None

        return super().address_record_to_dict(record)
