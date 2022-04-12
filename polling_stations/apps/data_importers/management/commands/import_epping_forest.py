from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EPP"
    addresses_name = (
        "2022-05-05/2022-03-29T13:45:31.095161/Democracy_Club__05May2022 EFDC.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-29T13:45:31.095161/Democracy_Club__05May2022 EFDC.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "CM16 6JA",
        ]:
            return None
        return super().address_record_to_dict(record)
