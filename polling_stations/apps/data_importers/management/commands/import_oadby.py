from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "OAD"
    addresses_name = "2021-03-16T16:05:47.817797/Democracy_Club__06May2021.csv"
    stations_name = "2021-03-16T16:05:47.817797/Democracy_Club__06May2021.csv"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100030597499",  # 69A LONG STREET, WIGSTON
            "10010149199",  # 67A LONG STREET, WIGSTON
            "100030597496",  # OADBY LODGE YOUTH HOSTEL GARTREE ROAD, OADBY
            "10010146840",  # 46A LONG STREET, WIGSTON
        ]:
            return None

        if record.addressline6 in ["LE18 2GQ"]:
            return None

        return super().address_record_to_dict(record)
