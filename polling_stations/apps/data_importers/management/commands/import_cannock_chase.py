from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CAN"
    addresses_name = (
        "2023-05-04/2023-03-16T12:03:23.219491/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-16T12:03:23.219491/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100032224228",  # 179 HEDNESFORD ROAD, HEATH HAYES, CANNOCK
        ]:
            return None

        if record.addressline6 in [
            # split
            "WS12 3YG",
            "WS11 9NW",
            # look wrong
            "WS11 1LF",
            "WS12 1RB",
        ]:
            return None

        return super().address_record_to_dict(record)
