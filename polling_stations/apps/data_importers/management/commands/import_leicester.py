from data_importers.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "LCE"
    addresses_name = (
        "2023-05-04/2023-03-09T11:16:48.756990/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-09T11:16:48.756990/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"
    station_postcode_search_fields = [
        "polling_place_postcode",
        "polling_place_address_4",
        "polling_place_address_3",
        "polling_place_address_2",
    ]

    def address_record_to_dict(self, record):
        if record.addressline6 in ["LE3 0FP", "LE1 7GT", "LE4", "LE4 2RD"]:
            return None

        return super().address_record_to_dict(record)
