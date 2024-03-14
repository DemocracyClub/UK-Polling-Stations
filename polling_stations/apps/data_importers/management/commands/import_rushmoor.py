from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RUH"
    addresses_name = (
        "2024-05-02/2024-03-14T10:25:53.338856/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-14T10:25:53.338856/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100062323099",  # GOLD FARM, GOVERNMENT ROAD, ALDERSHOT
        ]:
            return None

        return super().address_record_to_dict(record)
