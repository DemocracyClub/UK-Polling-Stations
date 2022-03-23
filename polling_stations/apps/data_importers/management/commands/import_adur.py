from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ADU"
    addresses_name = (
        "2022-05-05/2022-03-23T16:14:43.810437/Democracy_Club__05May2022ADC.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-23T16:14:43.810437/Democracy_Club__05May2022ADC.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "BN15 8BA",
            "BN43 6DF",
        ]:
            return None  # split

        return super().address_record_to_dict(record)
