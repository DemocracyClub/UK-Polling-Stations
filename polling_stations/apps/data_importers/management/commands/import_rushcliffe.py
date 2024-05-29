from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RUS"
    addresses_name = (
        "2024-07-04/2024-05-29T11:45:24.392981/Democracy_Club__04July2024.CSV"
    )
    stations_name = (
        "2024-07-04/2024-05-29T11:45:24.392981/Democracy_Club__04July2024.CSV"
    )
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "3040046674"  # WATERS EDGE, ZOUCH FARM, MAIN STREET, ZOUCH, LOUGHBOROUGH
        ]:
            return None

        if record.addressline6 in [
            # split
            "NG13 8GP",
            "NG2 5JT",
            "NG13 8DT",
        ]:
            return None

        return super().address_record_to_dict(record)
