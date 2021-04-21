from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TEW"
    addresses_name = (
        "2021-04-07T14:05:20.464410/Democracy_Club__06May2021_Tewkesbury Borough.tsv"
    )
    stations_name = (
        "2021-04-07T14:05:20.464410/Democracy_Club__06May2021_Tewkesbury Borough.tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6.strip() in [
            "WR12 7NA",
            "GL3 2HG",
            "GL53 9QR",
            "GL20 6JL",
            "GL52 9HN",
            "GL2 9FG",
            "GL3 4SX",
        ]:
            return None

        return super().address_record_to_dict(record)
