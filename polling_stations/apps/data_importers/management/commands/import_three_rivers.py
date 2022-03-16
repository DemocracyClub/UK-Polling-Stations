from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "THE"
    addresses_name = (
        "2022-05-05/2022-03-16T12:44:36.869968/Democracy_Club__05May2022-2.csv"
    )
    stations_name = (
        "2022-05-05/2022-03-16T12:44:36.869968/Democracy_Club__05May2022-2.csv"
    )
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):

        if record.addressline6 in [
            "WD19 4LS",
        ]:
            return None

        return super().address_record_to_dict(record)
