from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SEL"
    addresses_name = (
        "2022-05-05/2022-03-11T13:58:00.274589/Democracy_Club__05May2022-3.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-11T13:58:00.274589/Democracy_Club__05May2022-3.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "YO8 8FH",
            "LS24 9HH",
        ]:
            return None

        return super().address_record_to_dict(record)
