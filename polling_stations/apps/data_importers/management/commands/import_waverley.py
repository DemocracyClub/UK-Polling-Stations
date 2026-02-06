from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WAE"
    addresses_name = (
        "2026-05-07/2026-02-06T11:31:58.095008/Democracy_Club__07May2026.CSV"
    )
    stations_name = (
        "2026-05-07/2026-02-06T11:31:58.095008/Democracy_Club__07May2026.CSV"
    )
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100061602142",  # 3 FARNBOROUGH ROAD, FARNHAM
            "10096746074",  # FLAT 1, GAINSBOROUGH HOUSE, 204 HIGH STREET, CRANLEIGH
            "10096746075",  # FLAT 2, GAINSBOROUGH HOUSE, 204 HIGH STREET, CRANLEIGH
            "100061616831",  # KENNELS COTTAGE, HASLEMERE ROAD, WITLEY, GODALMING
        ]:
            return None

        if record.addressline6 in [
            "GU9 0NZ",  # split
            "RH12 3BQ",  # looks wrong
        ]:
            return None

        return super().address_record_to_dict(record)
