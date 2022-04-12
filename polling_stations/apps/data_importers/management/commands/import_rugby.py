from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RUG"
    addresses_name = (
        "2022-05-05/2022-03-29T12:58:01.553521/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-29T12:58:01.553521/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10010525228",  # 46 STATION AVENUE, HOULTON, RUGBY
        ]:
            return None

        return super().address_record_to_dict(record)
