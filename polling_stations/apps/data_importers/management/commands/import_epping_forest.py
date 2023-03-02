from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EPP"
    addresses_name = (
        "2023-05-04/2023-03-02T09:52:57.892038/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-02T09:52:57.892038/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10012157511",  # WALLED GARDEN HOUSE, EPPING
            "10012157510",  # TIMBER LODGE, EPPING
            "100091477396",  # SCHOOL HOUSE, KING HAROLD SCHOOL, BROOMSTICK HALL ROAD, WALTHAM ABBEY
            "100091478068",  # INNER LODGE, DOWDING WAY, WALTHAM ABBEY
            "10012158424",  # WALTHAM COMMON LOCK HOUSE, WINDMILL LANE, CHESHUNT, WALTHAM CROSS
            "100091249452",  # SHONKS FARM, MILL STREET, HARLOW
        ]:
            return None

        if record.addressline6 in [
            # splits
            "CM16 6JA",
        ]:
            return None

        return super().address_record_to_dict(record)
