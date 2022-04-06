from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BBD"
    addresses_name = (
        "2022-05-05/2022-03-24T16:15:31.261269/Democracy_Club__05May2022.CSV"
    )
    stations_name = (
        "2022-05-05/2022-03-24T16:15:31.261269/Democracy_Club__05May2022.CSV"
    )
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "BB1 7LS",
            "BB1 7LT",
            "BB1 2NL",
            "BB1 1EB",
            "BB3 2NQ",
        ]:
            return None
        return super().address_record_to_dict(record)
