from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MEL"
    addresses_name = (
        "2023-05-04/2023-05-03T13:04:51.058305/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-05-03T13:04:51.058305/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        if uprn in [
            "10002082195",  # 1 POTTER HILL, NOTTINGHAM ROAD, MELTON MOWBRAY
        ]:
            return None
        if record.addressline6 in [
            # split
            "NG32 1QG",
            "LE14 2XB",
            "NG32 1QQ",
            # not sure
            "LE14 4SS",
            "LE14 4SR",
        ]:
            return None

        return super().address_record_to_dict(record)
