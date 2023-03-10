from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SHO"
    addresses_name = (
        "2023-05-04/2023-03-10T10:02:51.770731/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-10T10:02:51.770731/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100030894500",  # BUSLEY, SOUTH DROVE, SPALDING
            "10094356949",  # LITTLE ACRE, SOUTH DROVE, SPALDING
            "100030888845",  # AMOW, MIDDLE MARSH ROAD, MOULTON MARSH, SPALDING
            "100030887883",  # 1 FARM COTTAGE, GEDNEY DYKE, SPALDING
            "100032311625",  # 2 FARM COTTAGE, GEDNEY DYKE, SPALDING
        ]:
            return None

        if record.addressline6 in [
            # split
            "PE12 9QJ",
            "PE11 4JH",
            "PE6 0LR",
        ]:
            return None

        return super().address_record_to_dict(record)
