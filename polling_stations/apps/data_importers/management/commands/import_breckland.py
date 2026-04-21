from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BRE"
    addresses_name = (
        "2026-05-07/2026-03-27T15:27:47.061067/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-27T15:27:47.061067/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "100091495478",  # M LAMBERT PLANT LTD, MILL POND FARM, THETFORD ROAD, GARBOLDISHAM, DISS
                "100091497149",  # 60 CROXTON ROAD, THETFORD
                "100091497209",  # CROXTON END, CROXTON ROAD, THETFORD
                "100091497248",  # ROSEISLE, CROXTON ROAD, THETFORD
                "10011976226",  # FAITHFIELDS, MAIN ROAD, LITTLE FRANSHAM, DEREHAM
                "10011976227",  # INDIGO HOUSE, MAIN ROAD, LITTLE FRANSHAM, DEREHAM
                "10011976228",  # LUNA HOUSE, MAIN ROAD, LITTLE FRANSHAM, DEREHAM
                "10011976645",  # HAWTHORNS, BOTTLE CORNER, BESTHORPE, ATTLEBOROUGH
                "10011992496",  # MAY CROFT, MAIN ROAD, LITTLE FRANSHAM, DEREHAM
                "10011992499",  # FIELDVIEW HOUSE, MAIN ROAD, LITTLE FRANSHAM, DEREHAM
                "10011992500",  # BRAMBLEWOOD, MAIN ROAD, LITTLE FRANSHAM, DEREHAM
                "10094466362",  # HEDGEROW, MAIN ROAD, LITTLE FRANSHAM, DEREHAM
                "10094466363",  # PARTRIDGE, MAIN ROAD, LITTLE FRANSHAM, DEREHAM
                "10094466365",  # OAKLANDS, MAIN ROAD, LITTLE FRANSHAM, DEREHAM
                "10094470114",  # 60C CROXTON ROAD, THETFORD
                "10096178957",  # WRENS NEST, MAIN ROAD, LITTLE FRANSHAM, DEREHAM
            ]
        ):
            return None

        if record.post_code in [
            # split
            "IP25 6HD",
            "IP25 6QX",
            "NR16 2AE",
            "NR17 1JX",
            "NR17 1QJ",
            "NR19 1EU",
            "NR19 1PS",
            "NR19 2LT",
            "NR20 3JS",
            "NR20 3QB",
            # suspect
            "PE37 7JP",  # SEA LORD CLOSE, SWAFFHAM
            "NR19 2FJ",  # LITTLE FRANSHAM, DEREHAM
            "IP24 2FR",  # DRYFIELD CLOSE, THETFORD
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # bugreport #627
        # coords change for: Dereham Town Football Club, Aldiss Park, Norwich Road, Dereham, NR20 3PX
        if record.polling_place_id == "15539":
            record = record._replace(
                polling_place_easting="601036", polling_place_northing="313508"
            )

        if record.polling_place_id in [
            "15784",  # Rocklands Village Hall The Street Rocklands
            "15900",  # Ovington Village Hall Church Road Ovington
            "15772",  # Oxborough Village Hall Swaffham Road Oxborough
        ]:
            # The E/N points are the wrong way round for these 3, perform the ol' switcheroo
            easting = record.polling_place_northing
            northing = record.polling_place_easting
            record = record._replace(polling_place_easting=easting)
            record = record._replace(polling_place_northing=northing)

        # Remove suspect coords for two stations at:
        # Thetford Church on the Way, Churchill Road, Thetford, IP24 2JZ
        if record.polling_place_id in [
            "15751",
            "15817",
        ]:
            record = record._replace(
                polling_place_easting="0",
                polling_place_northing="0",
            )
        # bugreport # 778
        # remove suspect coords for:
        # Arts Centre Hall at Aurora Eccles School, Quidenham Road, Quidenham, NR16 2NZ
        if record.polling_place_id == "15618":
            record = record._replace(
                polling_place_easting="0",
                polling_place_northing="0",
            )
        return super().station_record_to_dict(record)
