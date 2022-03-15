from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BAN"
    addresses_name = (
        "2022-05-05/2022-03-15T10:41:10.823370/Democracy_Club__05May2022.CSV"
    )
    stations_name = (
        "2022-05-05/2022-03-15T10:41:10.823370/Democracy_Club__05May2022.CSV"
    )
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "RG26 3SZ",
        ]:
            return None

        return super().address_record_to_dict(record)
