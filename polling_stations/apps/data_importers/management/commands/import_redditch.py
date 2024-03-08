from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RED"
    addresses_name = (
        "2024-05-02/2024-03-08T10:45:07.238107/Redditch Democracy_Club__02May2024.CSV"
    )
    stations_name = (
        "2024-05-02/2024-03-08T10:45:07.238107/Redditch Democracy_Club__02May2024.CSV"
    )
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100120639304",  # PARKLANDS CARE HOME, CALLOW HILL LANE, CALLOW HILL, REDDITCH
        ]:
            return None

        return super().address_record_to_dict(record)
