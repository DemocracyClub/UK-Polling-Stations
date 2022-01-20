from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SOS"
    addresses_name = "2022-01-13T16:25:37.997169/Democracy_Club__03February2022.tsv"
    stations_name = "2022-01-13T16:25:37.997169/Democracy_Club__03February2022.tsv"
    elections = ["2022-02-03"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "SS0 0NP",
            "SS2 6UY",
            "SS9 1LN",
            "SS9 1NH",
            "SS9 1QY",
            "SS9 1RP",
            "SS9 3BG" "SS9 3BG",
            "SS9 5EW",
        ]:
            return None

        return super().address_record_to_dict(record)
