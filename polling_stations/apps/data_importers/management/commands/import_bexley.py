from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BEX"
    addresses_name = (
        "2022-05-05/2022-03-10T09:24:15.450401/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-10T09:24:15.450401/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10094789367",  # 51A MAYPLACE ROAD WEST, BEXLEYHEATH
        ]:
            return None

        return super().address_record_to_dict(record)
