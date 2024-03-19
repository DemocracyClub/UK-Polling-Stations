from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "PLY"
    addresses_name = (
        "2024-05-02/2024-03-19T14:11:56.038006/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-19T14:11:56.038006/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100040493091",  # THE HOLLOW, TAMERTON FOLIOT ROAD, PLYMOUTH
            "10070767325",  # CANN LODGE, TAMERTON FOLIOT, PLYMOUTH
            "10070771403",  # FLAT 1, 24 DRINA LANE, PLYMOUTH
            "10070771404",  # FLAT 2, 24 DRINA LANE, PLYMOUTH
            "100040409446",  # LOWER GROUND FLOOR FLAT 11 ATHENAEUM STREET, PLYMOUTH
            "100040409450",  #  14A ATHENAEUM STREET, PLYMOUTH
            "10012062433",  # POINT COTTAGE, SALTRAM, PLYMOUTH
            "10091562408",  # 43 PLYMBRIDGE ROAD, PLYMPTON, PLYMOUTH
            "100040475894",  # 1 PLYMBRIDGE ROAD, PLYMPTON, PLYMOUTH
            "10094641493",  # FLAT 1, 16A COLEBROOK ROAD, PLYMPTON, PLYMOUTH
            "10094641494",  # FLAT 2, 16A COLEBROOK ROAD, PLYMPTON, PLYMOUTH
            "100040415376",  # FLAT A ELFORDE HOUSE BLANDFORD ROAD, PLYMOUTH
            "100040415377",  # FLAT B ELFORDE HOUSE BLANDFORD ROAD, PLYMOUTH
            "10094641036",  # FLAT ARMY RESERVE CENTRE BREST ROAD, PLYMOUTH
            "100040416933",  # THE ABBEYFIELD TAMAR EXTRA CARE SOCIETY, ABBEYFIELD TAMAR HOUSE, 11 BREST ROAD, DERRIFORD, PLYMOUTH
            "100040439817",  # FORDER COTTAGE, FORDER VALLEY ROAD, PLYMOUTH
            "100040439788",  # 65 FORD PARK ROAD, PLYMOUTH
            "100040482969",  # FIRST FLOOR FLAT 52 SALISBURY ROAD, PLYMOUTH
            "100040482972",  # HUNNY B FLORIST, 55 SALISBURY ROAD, PLYMOUTH
            "100040434952",  # CARETAKERS FLAT (FLAT 1) METHODIST CENTRAL HALL EASTLAKE STREET, PLYMOUTH
            "10091564022",  # FLAT 2 METHODIST CENTRAL HALL EASTLAKE STREET, PLYMOUTH
            "100040476103",  # 76 PLYMSTOCK ROAD, PLYMOUTH
            "100040476105",  # 79 PLYMSTOCK ROAD, PLYMOUTH
        ]:
            return None

        if record.addressline6 in [
            # splits
            "PL4 8BP",
            "PL3 6EP",
            "PL4 7QB",
            # suspect
            "PL2 3BL",  # WOLSELEY ROAD, PLYMOUTH
            "PL7 1UF",  # RIDGE ROAD, PLYMPTON, PLYMOUTH
            "PL7 1UE",  # HEATHER GRANGE RIDGE ROAD, PLYMOUTH
            "PL7 1AA",  # OSMAND GARDENS, PLYMOUTH
        ]:
            return None

        return super().address_record_to_dict(record)
