from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WDE"
    addresses_name = "2024-07-04/2024-06-24T08:08:18.645993/wde-combined.tsv"
    stations_name = "2024-07-04/2024-06-24T08:08:18.645993/wde-combined.tsv"
    elections = ["2024-07-04"]
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
            "EX20 2SD",
            "EX20 1SY",
            "EX20 2TP",
            "EX20 3NW",
            "EX20 1QB",
        ]:
            return None
        return super().address_record_to_dict(record)
