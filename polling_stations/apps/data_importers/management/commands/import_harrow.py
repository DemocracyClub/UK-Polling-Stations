from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HRW"
    addresses_name = "2021-03-25T11:47:14.508721/Democracy_Club__06May2021 - 2.tsv"
    stations_name = "2021-03-25T11:47:14.508721/Democracy_Club__06May2021 - 2.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6.strip() in ["HA1 2LH", "HA2 7SJ", "HA5 3HF", "HA5 2AB"]:
            return None

        return super().address_record_to_dict(record)
