from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CAN"
    addresses_name = (
        "2025-05-01/2025-03-06T09:46:47.909944/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-06T09:46:47.909944/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100032224228",  # 179 HEDNESFORD ROAD, HEATH HAYES, CANNOCK
            "10008161077",  # 85A CANNOCK ROAD, CANNOCK
            "100031617493",  # 22 BROWNHILLS ROAD, NORTON CANES, CANNOCK
        ]:
            return None

        if record.addressline6 in [
            # splits
            "WS12 3YG",
            "WS11 9NX",
            "WS11 9NW",
            # look wrong
            "WS11 9AD",
        ]:
            return None

        return super().address_record_to_dict(record)
