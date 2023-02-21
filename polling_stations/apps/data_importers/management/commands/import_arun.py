from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ARU"
    addresses_name = "2021-05-01T06:54:35.189732/Democracy_Club__06May2021(2).tsv"
    stations_name = "2021-05-01T06:54:35.189732/Democracy_Club__06May2021(2).tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in ["PO21 1JB"]:
            return None

        return super().address_record_to_dict(record)
