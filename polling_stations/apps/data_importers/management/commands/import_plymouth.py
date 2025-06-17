from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "PLY"
    addresses_name = "2025-07-17/2025-06-17T10:10:40.181606/Democracy Club Data.tsv"
    stations_name = "2025-07-17/2025-06-17T10:10:40.181606/Democracy Club Data.tsv"
    elections = ["2025-07-17"]
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
                "100040476103",  # 76 PLYMSTOCK ROAD, PLYMOUTH
                "100040476105",  # 79 PLYMSTOCK ROAD, PLYMOUTH
            ]
        ):
            return None

        if record.addressline6 in [
            # # splits
            "PL3 4HB",
            "PL4 8BP",
            "PL4 7QB",
            "PL3 6EP",
            # suspect
            "PL7 1UF",  # RIDGE ROAD, PLYMPTON, PLYMOUTH
            "PL7 1AA",  # OSMAND GARDENS, PLYMOUTH
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Adding missing polling place details the second station at the same polling place
        if record.polling_place_id == "8640":
            record = record._replace(
                polling_place_easting="246538",
                polling_place_northing="59085",
                polling_place_name="St. Francis of Assisi Church Hall",
            )

        return super().station_record_to_dict(record)
