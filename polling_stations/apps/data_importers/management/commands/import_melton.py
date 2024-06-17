from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MEL"
    addresses_name = (
        "2024-07-04/2024-06-17T11:41:17.871965/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-17T11:41:17.871965/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        if uprn in [
            "100032044579",  # GLEBE FARM, MAIN STREET, SAXELBY, MELTON MOWBRAY
            "100032044777",  # HILL FARM, EASTWELL ROAD, SCALFORD, MELTON MOWBRAY
            "10095606152",  # BRAMBLE BARN, EASTWELL ROAD, SCALFORD, MELTON MOWBRAY
        ]:
            return None
        if record.addressline6 in [
            # split
            "NG32 1QG",
            "LE14 2XB",
            "NG32 1QQ",
            # suspect
            "LE13 0SF",
        ]:
            return None

        return super().address_record_to_dict(record)
