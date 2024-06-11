from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HIL"
    addresses_name = (
        "2024-07-04/2024-06-11T08:46:39.957180/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-11T08:46:39.957180/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100022832219",  # 1 ELM VIEW HOUSE, SHEPISTON LANE, HAYES
            "100021415931",  # 33 BATH ROAD, HEATHROW, HOUNSLOW
            "100021415932",  # 35 ELM VIEW HOUSE, SHEPISTON LANE, HAYES
        ]:
            return None
        if record.addressline6 in [
            # split
            "UB4 9QN",
            "UB3 2FH",
            "UB3 3PF",
            "UB4 9QN",
            "UB8 3QT",
            "UB8 3FE",
            "UB8 3QD",
            "UB7 9GA",
        ]:
            return None
        return super().address_record_to_dict(record)
