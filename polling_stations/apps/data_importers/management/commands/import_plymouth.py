from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "PLY"
    addresses_name = (
        "2026-05-07/2026-03-04T16:37:36.094929/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-04T16:37:36.094929/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "100040493091",  # THE HOLLOW, TAMERTON FOLIOT ROAD, PLYMOUTH
                "10070771403",  # FLAT 1, 24 DRINA LANE, PLYMOUTH
                "10070771404",  # FLAT 2, 24 DRINA LANE, PLYMOUTH
                "100040409446",  # LOWER GROUND FLOOR FLAT 11 ATHENAEUM STREET, PLYMOUTH
                "10012062433",  # POINT COTTAGE, SALTRAM, PLYMOUTH
                "10091562408",  # 43 PLYMBRIDGE ROAD, PLYMPTON, PLYMOUTH
                "100040475894",  # 1 PLYMBRIDGE ROAD, PLYMPTON, PLYMOUTH
                "100040415376",  # FLAT A ELFORDE HOUSE BLANDFORD ROAD, PLYMOUTH
                "100040415377",  # FLAT B ELFORDE HOUSE BLANDFORD ROAD, PLYMOUTH
                "100040439788",  # 65 FORD PARK ROAD, PLYMOUTH
                "100040482969",  # FIRST FLOOR FLAT 52 SALISBURY ROAD, PLYMOUTH
                "100040482972",  # HUNNY B FLORIST, 55 SALISBURY ROAD, PLYMOUTH
                "100040434952",  # CARETAKERS FLAT (FLAT 1) METHODIST CENTRAL HALL EASTLAKE STREET, PLYMOUTH
                "10091564022",  # FLAT 2 METHODIST CENTRAL HALL EASTLAKE STREET, PLYMOUTH
            ]
        ):
            return None

        if record.addressline6 in [
            # splits
            "PL4 8BP",
            "PL3 4HB",
            # suspect
            "PL9 7PB",
            "PL1 4SG",
            "PL1 4DU",
            "PL1 4TH",
        ]:
            return None

        return super().address_record_to_dict(record)
