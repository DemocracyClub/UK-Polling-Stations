from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "PEN"
    addresses_name = (
        "2026-05-07/2026-02-16T16:37:15.618475/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-16T16:37:15.618475/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10022950288",  # PEARL COTTAGE, ALMA ROAD, COLNE
            "61014294",  # 117 EDWARD STREET, NELSON
            "100012400306",  # BROWN HOUSE FARM, GISBURN OLD ROAD, BLACKO, NELSON
        ]:
            return None

        if record.addressline6 in [
            # suspect
            "BB9 7YS",
        ]:
            return None

        return super().address_record_to_dict(record)
