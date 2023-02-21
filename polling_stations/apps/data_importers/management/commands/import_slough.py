from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SLG"
    addresses_name = (
        "2022-05-05/2022-04-07T09:34:53.056236/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-04-07T09:34:53.056236/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "SL2 2LZ",
            "SL3 7FU",
            "SL3 8QT",
            "SL1 2LT",
            "SL2 2DW",
        ]:
            return None

        return super().address_record_to_dict(record)
