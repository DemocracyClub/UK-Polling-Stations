from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WAE"
    addresses_name = (
        "2023-05-04/2023-03-06T13:52:11.644072/Democracy_Club__04May2023.CSV"
    )
    stations_name = (
        "2023-05-04/2023-03-06T13:52:11.644072/Democracy_Club__04May2023.CSV"
    )
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "GU8 5TE",
            "GU9 0NZ",
            "GU10 4BT",
            "GU9 8EU",
            "GU9 9JT",
            "RH12 3ZD",
        ]:
            return None

        return super().address_record_to_dict(record)
