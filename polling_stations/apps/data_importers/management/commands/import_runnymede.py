from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RUN"
    addresses_name = (
        "2026-05-07/2026-02-05T11:27:32.285822/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-05T11:27:32.285822/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10092963299",  # FLAT AT 79 STATION ROAD, ADDLESTONE
            "100062604551",  # ST. GEORGES COLLEGE, WEYBRIDGE ROAD, ADDLESTONE
        ]:
            return None
        if record.addressline6 in [
            "KT16 8AG",  # split
            "KT16 0AB",  # 10 WATERY LANE, CHERTSEY
        ]:
            return None

        return super().address_record_to_dict(record)
