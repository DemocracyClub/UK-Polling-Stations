from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ADU"
    addresses_name = (
        "2024-05-02/2024-03-11T13:14:29.911591/Democracy_Club__02May2024ADC.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-11T13:14:29.911591/Democracy_Club__02May2024ADC.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "BN43 6DF",
        ]:
            return None

        return super().address_record_to_dict(record)
