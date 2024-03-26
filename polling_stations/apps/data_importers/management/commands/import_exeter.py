from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EXE"
    addresses_name = "2024-05-02/2024-04-03T11:11:17.239870/Democracy_Club__02May2024-Exeter City.CSV"
    stations_name = "2024-05-02/2024-04-03T11:11:17.239870/Democracy_Club__02May2024-Exeter City.CSV"
    elections = ["2024-05-02"]

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
