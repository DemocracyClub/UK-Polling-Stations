from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "OAD"
    addresses_name = (
        "2023-05-04/2023-03-09T11:30:58.428015/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-09T11:30:58.428015/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100030597499",  # 69A LONG STREET, WIGSTON
            "10010149199",  # 67A LONG STREET, WIGSTON
            "100030597496",  # OADBY LODGE YOUTH HOSTEL GARTREE ROAD, OADBY
            "10010146840",  # 46A LONG STREET, WIGSTON
        ]:
            return None

        if record.addressline6 in ["LE18 2GQ", "LE18 4AB", "LE18 3AN"]:
            return None

        return super().address_record_to_dict(record)
