from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "CHO"
    addresses_name = "2023-05-04/2023-03-17T09:21:10.517030/Eros_SQL_Output008.csv"
    stations_name = "2023-05-04/2023-03-17T09:21:10.517030/Eros_SQL_Output008.csv"
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100010387618",  # MILLSTONE HOUSE, THE GREEN, ECCLESTON, CHORLEY
        ]:
            return None

        if record.housepostcode in [
            # split
            "PR7 2QL",
            "PR6 0HT",
            "PR6 0BS",
            # look wrong
            "PR26 9HE",
        ]:
            return None  # split

        return super().address_record_to_dict(record)
