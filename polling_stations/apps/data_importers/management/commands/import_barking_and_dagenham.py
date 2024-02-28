from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BDG"
    addresses_name = (
        "2024-05-02/2024-02-28T16:35:51.758530/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-02-28T16:35:51.758530/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100048739",  # 13 STANLEY AVENUE, BARKING
            "100092520",  # SHIP AND SHOVEL RIPPLE ROAD, BARKING
            "10023598442",  # 36A WHALEBONE LANE SOUTH, DAGENHAM
            "10023592360",  # 32A WHALEBONE LANE SOUTH, DAGENHAM
            "10023598812",  # 8A ROYAL PARADE, CHURCH STREET, DAGENHAM
        ]:
            return None

        if record.addressline6 in [
            # splits
            "IG11 7EX",
            "RM9 6GP",
            "IG11 7XS",
            "RM8 3PT",
            # looks wrong
            "RM9 6GJ",
            "IG11 0SR",
        ]:
            return None

        return super().address_record_to_dict(record)
