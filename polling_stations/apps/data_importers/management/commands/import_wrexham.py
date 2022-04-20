from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WRX"
    addresses_name = (
        "2022-05-05/2022-04-20T12:48:21.082477/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-04-20T12:48:21.082477/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "LL13 0YU",
            "LL13 9EN",
            "LL11 4UY",
            "LL13 8US",
            "LL12 0RY",
            "LL13 0HP",
            "LL12 9YG",
        ]:
            return None  # split

        return super().address_record_to_dict(record)
