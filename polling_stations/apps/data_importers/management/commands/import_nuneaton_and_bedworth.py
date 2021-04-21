from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NUN"
    addresses_name = "2021-04-08T14:20:43.445604/Democracy_Club__06May2021.tsv"
    stations_name = "2021-04-08T14:20:43.445604/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6.strip() in [
            "CV10 7BE",
            "CV10 9QF",
            "CV12 9HJ",
            "CV7 9NQ",
            "CV11 6NL",
            "CV11 6JF",
            "CV11 6JE",
            "CV11 4NW",
            "CV10 9FG",
        ]:
            return None  # split

        return super().address_record_to_dict(record)
