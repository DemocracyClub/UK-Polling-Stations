from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HIL"
    addresses_name = (
        "2026-05-07/2026-03-30T10:19:19.848410/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-30T10:19:19.848410/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100022832219",  # 1 ELM VIEW HOUSE, SHEPISTON LANE, HAYES
            "100021415931",  # 33 BATH ROAD, HEATHROW, HOUNSLOW
            "100021415932",  # 35 ELM VIEW HOUSE, SHEPISTON LANE, HAYES
            "10096324795",  # 1 GRAINFIELD WALK, EASTCOTE
        ]:
            return None
        if record.addressline6 in [
            # split
            "UB8 3FE",
            "UB3 2FH",
            "UB8 3QT",
            "UB7 9GA",
            "UB8 3JH",
            "UB3 3PF",
            "UB3 5HX",
            "UB8 3QD",
            "UB4 9QN",
            # suspect
            "UB4 8QJ",
            "UB4 8QL",
        ]:
            return None
        return super().address_record_to_dict(record)
