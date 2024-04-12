from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WDE"
    addresses_name = (
        "2024-05-02/2024-04-12T09:18:24.145364/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-04-12T09:18:24.145364/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10001332226",  # ROWDEN, BRIDESTOWE, OKEHAMPTON
            "10001330732",  # HOMEFIELD, DREWSTEIGNTON, EXETER
            "10001322729",  # SOUTH MOOR, JACOBSTOWE, OKEHAMPTON
            "10001322728",  # SOUTHMOOR FARM ROAD FROM LANGABEAR MOOR TO SOUTHMOOR FARM, JACOBSTOWE
        ]:
            return None
        if record.addressline6 in [
            # split
            "EX20 2TP",
            "EX20 1QB",
            "EX20 1SY",
            "EX20 3NW",
            "EX20 2SD",
        ]:
            return None
        return super().address_record_to_dict(record)
