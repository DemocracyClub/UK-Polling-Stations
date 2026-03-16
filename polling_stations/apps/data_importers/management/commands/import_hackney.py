from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HCK"
    addresses_name = (
        "2026-05-07/2026-03-16T14:58:22.779090/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-16T14:58:22.779090/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10008342758",  # 20 MILLFIELDS PARADE, MILLFIELDS ROAD, LONDON
                "10008354539",  # 22 MILLFIELDS PARADE, MILLFIELDS ROAD, LONDON
                "200001073528",  # POTTERY HOUSE, ELRINGTON ROAD, LONDON
                "10008353260",  # 1A SHEPHERDESS WALK, LONDON
                "10008353261",  # 1C SHEPHERDESS WALK, LONDON
                "100023136742",  # 5 SHEPHERDESS WALK, LONDON
                "10008300094",  # CARETAKERS PREMISES JUBILEE PRIMARY SCHOOL FILEY AVENUE, HACKNEY, LONDON
                "10008224605",  # TURKISH CYPRIOT COMMUNITY ASSOCIATION, 117 GREEN LANES, LONDON
            ]
        ):
            return None

        if record.addressline6 in [
            # split
            "E5 8AF",
            "E8 4PB",
            "N16 7UY",
            "N16 8NT",
            # suspect
            "N16 5TU",
        ]:
            return None
        return super().address_record_to_dict(record)
