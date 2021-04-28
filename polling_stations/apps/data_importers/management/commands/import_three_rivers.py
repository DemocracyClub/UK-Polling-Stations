from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "THE"
    addresses_name = (
        "2021-04-20T10:19:27.612662/Three rivers Democracy_Club__06May2021.tsv"
    )
    stations_name = (
        "2021-04-20T10:19:27.612662/Three rivers Democracy_Club__06May2021.tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "latin-1"

    def address_record_to_dict(self, record):

        if record.addressline6 in ["WD3 5HD", "WD25 0JX", "WD19 7BU"]:
            return None

        return super().address_record_to_dict(record)
