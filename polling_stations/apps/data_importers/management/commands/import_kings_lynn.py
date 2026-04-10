from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KIN"
    addresses_name = (
        "2026-05-07/2026-04-10T09:26:35.937043/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-04-10T09:26:35.937043/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10000033946",  # 81B HIGH STREET, KING'S LYNN
            "10090917704",  # 199 STATION ROAD, WATLINGTON, KING'S LYNN
        ]:
            return None
        if record.addressline6 in [
            # split
            "PE33 9FZ",
            "PE30 5FP",
            "PE30 5BD",
            # look wrong
            "PE30 1JG",
        ]:
            return None

        return super().address_record_to_dict(record)
