from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SND"
    addresses_name = (
        "2023-05-04/2023-04-05T14:43:52.611477/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-05T14:43:52.611477/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "DH4 7RD",
            "SR2 0AQ",
            "SR2 9JG",
            "SR4 8JF",
            "DH4 5HY",
            "SR2 8RA",
            "SR5 3EP",
            "SR4 6NP",
            "DH4 4JH",
            "SR6 9DY",
            "SR2 7HZ",
            "SR2 0LE",
            "SR4 7SD",
            "SR3 1XF",
            "DH4 6SN",
            "SR4 0BT",
            "SR4 8HA",
            "DH4 4FL",
            "SR4 8JU",
            "SR6 0NB",
            "SR3 3QH",
        ]:
            return None
        return super().address_record_to_dict(record)
