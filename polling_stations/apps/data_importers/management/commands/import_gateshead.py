from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "GAT"
    addresses_name = (
        "2026-05-07/2026-02-06T07:56:31.998058/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-06T07:56:31.998058/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "100000002781",  # RIDING CHASE, NORMANS RIDING POULTRY FARM, BLAYDON-ON-TYNE
                "10022984423",  # HIGH EIGHTON FARM HOUSE BLACK LANE, HARLOW GREEN, GATESHEAD
                "100000074532",  # CHEVVY CHASE, PENNYFINE ROAD, SUNNISIDE, NEWCASTLE UPON TYNE
                "100000074529",  # 130 PENNYFINE ROAD, SUNNISIDE, NEWCASTLE UPON TYNE
            ]
        ):
            return None

        if record.addressline6 in [
            # looks wrong
            "NE10 9HL",
        ]:
            return None

        return super().address_record_to_dict(record)
