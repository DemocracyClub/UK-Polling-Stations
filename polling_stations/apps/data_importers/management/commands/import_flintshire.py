from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "FLN"
    addresses_name = (
        "2021-03-29T09:58:34.913328/Flintshire Democracy_Club__06May2021.tsv"
    )
    stations_name = (
        "2021-03-29T09:58:34.913328/Flintshire Democracy_Club__06May2021.tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "CH5 3AR",
            "CH5 3ER",
            "CH5 3ES",
            "CH5 3DL",
            "CH4 0PE",
            "CH4 0PT",
            "CH7 2ED",
            "CH7 2JP",
            "CH7 2PU",
            "CH7 3LH",
            "CH7 6LG",
            "CH7 2JR",
            "CH7 3NG",
            "CH7 3JU",
            "CH7 3JQ",
            "CH7 6RH",
            "CH5 3EF",
            "LL12 9DU",
            "LL12 9AE",
            "LL12 9EF",
            "LL12 9HN",
            "LL12 9DG",
            "CH5 3LY",
            "CH5 3LZ",
            "CH5 3EH",
            "LL12 9AY",
            "LL12 9HE",
            "CH5 3PF",
            "CH5 1QR",
            "CH5 1PD",
            "CH7 5PW",
            "CH8 8LR",
            "CH8 8NY",
            "CH8 8NF",
            "CH7 5RD",
            "CH8 8JG",
            "CH8 8PP",
            "CH7 6PA",
            "CH8 8JN",
            "CH7 5DJ",
            "CH6 5TP",
            "CH8 7EZ",
            "CH8 7ED",
            "CH7 5JS",
            "CH8 8DL",
            "CH8 8JY",
            "CH8 8DF",
            "CH8 8HE",
            "CH8 8LG",
            "CH8 7SJ",
            "CH8 7NT",
            "CH8 7PG",
            "CH8 7PQ",
            "CH7 6QQ",
            "CH8 9AE",
            "CH8 9AW",
            "CH7 6TH",
            "CH7 6SD",
            "CH7 6YX",
            "CH7 6LQ",
            "CH7 6EH",
            "CH7 6BA",
            "CH7 6AH",
        ]:
            return None  # split

        if record.addressline6 == "CH7 2QC":
            record = record._replace(addressline6="CH7 2QG")

        if record.addressline6 == "CH4 0TO":
            record = record._replace(addressline6="CH4 0TP")

        return super().address_record_to_dict(record)
