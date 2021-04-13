from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SOS"
    addresses_name = "2021-03-29T13:06:29.813153/Southend.csv"
    stations_name = "2021-03-29T13:06:29.813153/Southend.csv"
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "SS0 7JG",
            "SS1 2PE",
            "SS9 4RP",
            "SS0 0BD",
            "SS0 8LL",
            "SS0 9HW",
            "SS1 2ER",
            "SS1 2TD",
            "SS2 6UY",
            "SS3 9QH",
            "SS9 1NH",
            "SS9 1QY",
            "SS9 1RP",
            "SS9 1SP",
            "SS9 2HE",
            "SS9 2PP",
            "SS9 3BG",
            "SS9 3NQ",
            "SS9 5EW",
            "SS3 9RJ",
        ]:
            return None

        return super().address_record_to_dict(record)
