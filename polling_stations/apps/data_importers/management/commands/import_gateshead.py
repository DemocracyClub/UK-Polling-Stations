from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "GAT"
    addresses_name = (
        "2022-05-05/2022-03-16T12:09:15.983600/Democracy_Club__05May2022.CSV"
    )
    stations_name = (
        "2022-05-05/2022-03-16T12:09:15.983600/Democracy_Club__05May2022.CSV"
    )
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "NE9 5XP",
            "NE9 6JR",
        ]:
            return None

        return super().address_record_to_dict(record)
