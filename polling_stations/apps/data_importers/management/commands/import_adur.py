from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ADU"
    addresses_name = "2021-02-15T11:20:20.221841/ADCDemocracy_Club__06May2021.tsv"
    stations_name = "2021-02-15T11:20:20.221841/ADCDemocracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 == "BN43 6DF":
            return None

        return super().address_record_to_dict(record)
