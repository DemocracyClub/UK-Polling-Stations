from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SOS"
    addresses_name = (
        "2024-07-04/2024-06-13T11:16:47.619894/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-13T11:16:47.619894/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "SS9 4RP",
            "SS9 1QY",
            "SS9 1LN",
            "SS9 1RP",
            "SS9 1NH",
            "SS3 9QH",
            "SS9 5EW",
        ]:
            return None

        return super().address_record_to_dict(record)
