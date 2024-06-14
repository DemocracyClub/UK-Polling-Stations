from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RCC"
    addresses_name = (
        "2024-07-04/2024-06-14T15:47:03.892737/Democracy_Club__04July2024.CSV"
    )
    stations_name = (
        "2024-07-04/2024-06-14T15:47:03.892737/Democracy_Club__04July2024.CSV"
    )
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10034529362",  # LIVERTON MILL, MOORSHOLM, SALTBURN-BY-THE-SEA
        ]:
            return None

        if record.addressline6 in [
            # split
            "TS10 4AJ",
            "TS6 0PA",
            # suspect
            "TS7 9HR",
        ]:
            return None

        return super().address_record_to_dict(record)
