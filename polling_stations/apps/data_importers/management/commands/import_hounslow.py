from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HNS"
    addresses_name = (
        "2021-04-01T10:43:33.063903/Democracy_Club__06May2021 - Hounslow.CSV"
    )
    stations_name = (
        "2021-04-01T10:43:33.063903/Democracy_Club__06May2021 - Hounslow.CSV"
    )
    elections = ["2021-05-06"]
    csv_delimiter = ","
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100021554382",  # 104 MARTINDALE ROAD, HOUNSLOW
            "100021539525",  # 208B BATH ROAD, HOUNSLOW
            "10090801431",  # FLAT 5 95 MASWELL PARK ROAD, HOUNSLOW
            "10090801430",  # FLAT 4 95 MASWELL PARK ROAD, HOUNSLOW
            "100021580780",  # FLAT 2 392 CHISWICK HIGH ROAD, CHISWICK, LONDON
            "100021514552",  # FLAT 1 36 HAMILTON ROAD, BRENTFORD
        ]:
            return None

        if record.addressline6 in [
            "TW4 6DH",
            "TW3 3DW",
            "TW3 3TU",
            "TW13 5JE",
            "W4 4EU",
            "TW13 6AB",
        ]:
            return None

        return super().address_record_to_dict(record)
