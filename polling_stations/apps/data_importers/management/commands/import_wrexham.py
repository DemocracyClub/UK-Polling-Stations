from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WRX"
    addresses_name = (
        "2021-03-31T21:21:48.762291/Wrexham New Democracy_Club__06May2021.tsv"
    )
    stations_name = (
        "2021-03-31T21:21:48.762291/Wrexham New Democracy_Club__06May2021.tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "LL13 0AW",
            "SY14 7LL",
            "LL13 0SF",
            "SY14 7LB",
            "SY13 3BU",
            "SY13 3DS",
            "LL13 0DA",
            "LL13 0DW",
            "LL13 0LS",
            "LL13 0TT",
            "SY13 3DR",
            "LL14 4LU",
            "LL14 3BH",
            "LL14 3BJ",
            "LL14 3RD",
            "LL20 7DD",
            "LL20 7HJ",
            "LL12 0RY",
            "LL12 8RH",
            "LL12 8SG",
            "LL12 8NT",
            "LL11 4UY",
            "LL11 4AP",
            "LL11 4HB",
            "LL13 8US",
            "LL13 0JW",
            "LL13 9EN",
            "LL13 9ND",
            "LL13 9NB",
            "LL11 4AH",
            "LL13 7TB",
        ]:
            return None  # split

        return super().address_record_to_dict(record)
