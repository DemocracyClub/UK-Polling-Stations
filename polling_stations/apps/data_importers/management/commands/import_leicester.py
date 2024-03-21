from data_importers.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "LCE"
    addresses_name = (
        "2024-05-02/2024-03-21T08:36:01.342545/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-21T08:36:01.342545/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    station_postcode_search_fields = [
        "polling_place_postcode",
        "polling_place_address_4",
        "polling_place_address_3",
        "polling_place_address_2",
    ]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "2465215460",  # 1A SACHEVERELL ROAD, LEICESTER
        ]:
            return None
        if record.addressline6 in [
            # split
            "LE1 7GT",
            "LE4",
            # suspect
            "LE4 2RD",
        ]:
            return None
        return super().address_record_to_dict(record)
