from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KWL"
    addresses_name = "2021-03-24T11:07:23.789553/Knowsley Democracy_Club__06May2021.CSV"
    stations_name = "2021-03-24T11:07:23.789553/Knowsley Democracy_Club__06May2021.CSV"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        if record.addressline6 in ["L34 1LP", "L36 5YR", "L35 1QN"]:
            return None

        return super().address_record_to_dict(record)
