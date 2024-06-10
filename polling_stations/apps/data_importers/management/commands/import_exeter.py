from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EXE"
    addresses_name = (
        "2024-07-04/2024-06-10T15:56:47.388239/Democracy_Club__04July2024 (15).tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-10T15:56:47.388239/Democracy_Club__04July2024 (15).tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10094735127",  # 1 COLLINGWOOD CLOSE, TOPSHAM, EXETER
            "10094735128",  # 2 COLLINGWOOD CLOSE, TOPSHAM, EXETER
            "10023121146",  # 210A TOPSHAM ROAD, EXETER
            "10091473295",  # EXE VIEW LODGE, STOKE HILL, EXETER
            "10094202708",  # THE OLD MESS ROOM, ST. MARKS AVENUE, EXETER
        ]:
            return None

        if record.addressline6 in [
            # split
            "EX2 7AY",
            "EX4 9HE",
            "EX4 5AJ",
            "EX2 7TF",
        ]:
            return None
        return super().address_record_to_dict(record)
