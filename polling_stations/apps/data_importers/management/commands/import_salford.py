from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SLF"
    addresses_name = "2022-05-05/2022-03-29T11:40:42.009781/Democracy_Club__05May2022 - Salford City Council.tsv"
    stations_name = "2022-05-05/2022-03-29T11:40:42.009781/Democracy_Club__05May2022 - Salford City Council.tsv"
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):

        if record.addressline6 in ["M27 0JE"]:
            return None

        return super().address_record_to_dict(record)
