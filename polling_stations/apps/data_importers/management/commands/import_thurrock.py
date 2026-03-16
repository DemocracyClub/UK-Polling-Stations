from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "THR"
    addresses_name = (
        "2026-05-07/2026-03-16T14:11:49.479694/Democracy_Club__07May2026 (3).tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-16T14:11:49.479694/Democracy_Club__07May2026 (3).tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "100091301767",  # FLINT COTTAGE, MOLLANDS LANE, SOUTH OCKENDON
                "200001546102",  # LANGDON HALL FARM, OLD CHURCH HILL, LANGDON HILLS, BASILDON
                "100091297871",  # HOB HILL FARM, BIGGIN LANE, GRAYS
                "10095908244",  # 251 BRANKSOME AVENUE, STANFORD-LE-HOPE
            ]
        ):
            return None

        if record.addressline6.strip() in [
            # splits
            "RM17 5JZ",
        ]:
            return None

        return super().address_record_to_dict(record)
