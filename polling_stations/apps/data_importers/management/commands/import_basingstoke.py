from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BAN"
    addresses_name = "2021-03-03T11:11:11.274664/Basingstoke and Deane Democracy_Club__06May2021 (1).tsv"
    stations_name = "2021-03-03T11:11:11.274664/Basingstoke and Deane Democracy_Club__06May2021 (1).tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in ["RG26 3SZ"]:
            return None

        return super().address_record_to_dict(record)
