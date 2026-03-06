from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RUH"
    addresses_name = (
        "2026-05-07/2026-03-06T12:53:17.844890/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-06T12:53:17.844890/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100062323845",  # 259 NORTH LANE, ALDERSHOT, GU12 4SU
            "100062323099",  # GOLD FARM, GOVERNMENT ROAD, ALDERSHOT
        ]:
            return None

        return super().address_record_to_dict(record)
