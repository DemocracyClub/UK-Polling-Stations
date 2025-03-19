from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WDE"
    addresses_name = (
        "2025-05-01/2025-03-19T17:07:01.840411/Democracy_Club__01May2025 (3).tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-19T17:07:01.840411/Democracy_Club__01May2025 (3).tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10001332226",  # ROWDEN, BRIDESTOWE, OKEHAMPTON
                "10001330732",  # HOMEFIELD, DREWSTEIGNTON, EXETER
                "10001322729",  # SOUTH MOOR, JACOBSTOWE, OKEHAMPTON
                "10001322728",  # SOUTHMOOR FARM ROAD FROM LANGABEAR MOOR TO SOUTHMOOR FARM, JACOBSTOWE
                "10013751665",  # BERRYDOWN STABLES, EXBOURNE, OKEHAMPTON
                "100040396098",  # LITTLE GREENSLADE, SAMPFORD COURTENAY, OKEHAMPTON
            ]
        ):
            return None
        if record.addressline6 in [
            # split
            "EX20 1SY",
            "PL20 7DN",
            "EX20 3NW",
            "EX20 2TP",
            "EX20 1QB",
            "EX20 2SD",
        ]:
            return None
        return super().address_record_to_dict(record)
