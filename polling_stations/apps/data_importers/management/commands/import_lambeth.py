from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "LBH"
    addresses_name = (
        "2022-05-05/2022-03-29T12:35:09.475993/LBDemocracy_Club__05May2022_2.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-29T12:35:09.475993/LBDemocracy_Club__05May2022_2.tsv"
    )
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "SE11 5UG",
            "SW2 5RS",
        ]:
            return None

        return super().address_record_to_dict(record)
