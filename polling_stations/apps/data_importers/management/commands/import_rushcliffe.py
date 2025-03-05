from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RUS"
    addresses_name = (
        "2025-05-01/2025-03-05T11:39:23.992685/Democracy_Club__01May2025.CSV"
    )
    stations_name = (
        "2025-05-01/2025-03-05T11:39:23.992685/Democracy_Club__01May2025.CSV"
    )
    elections = ["2025-05-01"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        if uprn in [
            "3040046674",  # WATERS EDGE, ZOUCH FARM, MAIN STREET, ZOUCH, LOUGHBOROUGH
            "3040027189",  # 19-21 MAIN STREET, KEYWORTH, NOTTINGHAM
        ]:
            return None

        if record.addressline6 in [
            # split
            "NG13 7BT",
            "NG13 8GP",
            "NG2 5JT",
            "NG13 8DT",
        ]:
            return None

        return super().address_record_to_dict(record)
