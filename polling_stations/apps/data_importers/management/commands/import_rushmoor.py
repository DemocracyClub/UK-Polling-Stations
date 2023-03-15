from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RUH"
    addresses_name = (
        "2023-05-04/2023-03-15T16:53:47.237360/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-15T16:53:47.237360/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100062006907",  # 1B WATERLOO ROAD, ALDERSHOT
            "100062323687",  # 1 WATERLOO ROAD, ALDERSHOT
            "100062323733",  # 1A WATERLOO ROAD, ALDERSHOT
            "100062323188",  # YELLOW RIVER, 50 GROSVENOR ROAD, ALDERSHOT
        ]:
            return None

        return super().address_record_to_dict(record)
