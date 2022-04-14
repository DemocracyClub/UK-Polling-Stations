from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SND"
    addresses_name = (
        "2022-05-05/2022-04-14T10:32:28.104443/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-04-14T10:32:28.104443/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):

        if record.addressline6 in [
            "SR2 7HZ",
            "DH4 5HY",
            "SR2 0AQ",
            "DH4 7RD",
            "SR4 7SD",
            "SR2 0LE",
            "SR4 0BT",
            "SR2 9JG",
            "SR3 1XF",
            "SR6 9DY",
            "SR6 0NB",
            "SR5 3EP",
            "SR4 8JF",
            "DH4 4JH",
            "SR4 6NP",
            "SR4 8HA",
            "SR2 8RA",
            "SR4 8JU",
            "SR3 3QH",
        ]:
            return None
        return super().address_record_to_dict(record)
