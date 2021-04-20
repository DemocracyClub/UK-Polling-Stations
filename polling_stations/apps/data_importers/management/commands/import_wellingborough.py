from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WEL"
    addresses_name = (
        "2021-03-31T10:18:02.280304/Wellingborough Democracy_Club__06May2021 (2).tsv"
    )
    stations_name = (
        "2021-03-31T10:18:02.280304/Wellingborough Democracy_Club__06May2021 (2).tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "NN8 3JX",
            "NN29 7NL",
            "NN29 7AW",
            "NN8 4WG",
            "NN8 1SH",
            "NN7 1NP",
            "NN6 0FT",
        ]:
            return None  # split

        if record.property_urn.lstrip(" 0") in [
            "10024133595",  # long distance to polling station; leads to NN6 0FT split
        ]:
            return None

        return super().address_record_to_dict(record)
