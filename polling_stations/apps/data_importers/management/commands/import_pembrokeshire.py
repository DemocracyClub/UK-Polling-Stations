from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "PEM"
    addresses_name = "2024-05-02/2024-03-25T14:51:07.747895/Eros_SQL_Output001.csv"
    stations_name = "2024-05-02/2024-03-25T14:51:07.747895/Eros_SQL_Output001.csv"
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        record.uprn.strip().lstrip("0")
        if record.uprn in [
            "200003255203",  # LOWER FLAT, FERN HOUSE, WARREN STREET, TENBY
        ]:
            return None
        if record.housepostcode in [
            # split
            "SA73 2EB",
            "SA62 4NJ",
            "SA73 3RA",
            "SA68 0XN",
            "SA73 1NR",
            "SA62 3PW",
            "SA71 5BP",
            "SA73 1BB",
            "SA68 0QR",
            "SA73 1RG",
            "SA73 3HF",
            "SA62 5RJ",
            "SA72 6BH",
            "SA72 6BE",
            "SA62 5UD",
            "SA67 8RY",
            "SA62 5DB",
            "SA62 6TD",
            "SA62 5NL",
            "SA73 1RJ",
            "SA66 7QW",
        ]:
            return None
        return super().address_record_to_dict(record)
