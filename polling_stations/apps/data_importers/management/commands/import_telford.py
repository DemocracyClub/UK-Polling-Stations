from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TFW"
    addresses_name = "2021-04-28T15:13:31.221139/telford-deduped-mk2.tsv"
    stations_name = "2021-04-28T15:13:31.221139/telford-deduped-mk2.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "TF4 3JZ",
            "TF8 7NN",
            "TF2 8SF",
            "TF10 7RG",
            "TF2 7PE",
        ]:
            return None

        return super().address_record_to_dict(record)
