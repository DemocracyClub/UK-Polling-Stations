from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAS"
    addresses_name = (
        "2025-05-01/2025-03-10T10:23:31.659610/Democracy_Club__01May2025.CSV"
    )
    stations_name = (
        "2025-05-01/2025-03-10T10:23:31.659610/Democracy_Club__01May2025.CSV"
    )
    elections = ["2025-05-01"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10091487792",  # 65 CROMWELL STREET, MANSFIELD
            "10023935274",  # 31 BIRCHLANDS, FOREST TOWN, MANSFIELD
            "10096388538",  # 72 BIFROST BOULEVARD, WARSOP
            "10096388523",  # 17 KEMPTON ROAD, MANSFIELD
        ]:
            return None

        if record.addressline6 in [
            # splits
            "NG19 6AT",
            # looks wrong
            "NG18 4TG",
            # Council confirmed correct: NG18 6BH
        ]:
            return None

        return super().address_record_to_dict(record)
