from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RIC"
    addresses_name = "2021-04-16T09:27:30.944565/Democracy_Club__06May2021.tsv"
    stations_name = "2021-04-16T09:27:30.944565/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "TW12 2SB",
            "SW13 9RF",
        ]:
            return None

        return super().address_record_to_dict(record)
