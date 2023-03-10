from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TRF"
    addresses_name = (
        "2023-05-04/2023-03-10T13:25:57.792849/Democracy_Club__04May2023.CSV"
    )
    stations_name = (
        "2023-05-04/2023-03-10T13:25:57.792849/Democracy_Club__04May2023.CSV"
    )
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10070405338",  # 183A CROSS STREET, SALE
        ]:
            return None

        if record.addressline6 in [
            # split
            "M33 2BT",
            "WA14 4AN",
            "M33 3GG",
            "M33 5GN",
            "M33 2NL",
        ]:
            return None

        return super().address_record_to_dict(record)
