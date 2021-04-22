from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BRC"
    addresses_name = "2021-04-12T13:33:17.499979/Democracy_Club__06May2021.tsv"
    stations_name = "2021-04-12T13:33:17.499979/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "RG42 6HB",
            "RG42 6BX",
            "SL5 8DH",
            "RG12 9TH",
            "RG40 3YZ",
        ]:
            return None

        return super().address_record_to_dict(record)
