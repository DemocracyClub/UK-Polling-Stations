from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ASH"
    addresses_name = (
        "2023-05-04/2023-03-13T11:02:12.723251/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-13T11:02:12.723251/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100031248754",  # 31 COXMOOR ROAD, SUTTON-IN-ASHFIELD
        ]:
            return None

        if record.addressline6 in [
            # split
            "NG17 8BE",
            "NG17 5HS",
            # wrong
            "NG17 8JR",
            "NG17 5HS",
        ]:
            return None

        return super().address_record_to_dict(record)
