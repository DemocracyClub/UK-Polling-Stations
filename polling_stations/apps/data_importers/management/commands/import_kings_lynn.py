from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KIN"
    addresses_name = (
        "2024-07-04/2024-05-29T08:55:20.820012/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-29T08:55:20.820012/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10000033946",  # 81B HIGH STREET, KING'S LYNN
            "10090917704",  # 199 STATION ROAD, WATLINGTON, KING'S LYNN
            "10013001170",  # WHITE DYKE BUNGALOW, BLACK DYKE ROAD, HOCKWOLD, THETFORD
        ]:
            return None
        if record.addressline6 in [
            # split
            "PE30 5BD",
            # look wrong
            "PE30 1JG",
        ]:
            return None

        return super().address_record_to_dict(record)
