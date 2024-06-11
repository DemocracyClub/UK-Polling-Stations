from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RUH"
    addresses_name = (
        "2024-07-04/2024-06-11T09:44:37.221736/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-11T09:44:37.221736/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100062323099",  # GOLD FARM, GOVERNMENT ROAD, ALDERSHOT
        ]:
            return None

        return super().address_record_to_dict(record)
