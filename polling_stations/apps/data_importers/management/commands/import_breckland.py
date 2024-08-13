from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BRE"
    addresses_name = (
        "2024-07-04/2024-06-27T11:14:42.791023/Democracy_Club__04July2024.CSV"
    )
    stations_name = (
        "2024-07-04/2024-06-27T11:14:42.791023/Democracy_Club__04July2024.CSV"
    )
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "100091495478",  # M LAMBERT PLANT LTD, MILL POND FARM, THETFORD ROAD, GARBOLDISHAM, DISS
                "10011976645",  # HAWTHORNS, BOTTLE CORNER, BESTHORPE, ATTLEBOROUGH
                "10011990571",  # THE SPINNEY, SCHOOL ROAD, BRISLEY, DEREHAM
                "10011967701",  # THE GRANARY, LING ROAD, NORTH LOPHAM, DISS
                "100091497149",  # 60 CROXTON ROAD, THETFORD
                "10094470114",  # 60C CROXTON ROAD, THETFORD
                "100091497248",  # ROSEISLE, CROXTON ROAD, THETFORD
                "100091497209",  # CROXTON END, CROXTON ROAD, THETFORD
                "10011992994",  # WRETHAM MANOR ANNEXE CHURCH ROAD, WRETHAM
                "10011976226",  # FAITHFIELDS, MAIN ROAD, LITTLE FRANSHAM, DEREHAM
                "10011976227",  # INDIGO HOUSE, MAIN ROAD, LITTLE FRANSHAM, DEREHAM
                "10011976228",  # LUNA HOUSE, MAIN ROAD, LITTLE FRANSHAM, DEREHAM
                "10011992496",  # MAY CROFT, MAIN ROAD, LITTLE FRANSHAM, DEREHAM
                "10011992499",  # FIELDVIEW HOUSE, MAIN ROAD, LITTLE FRANSHAM, DEREHAM
                "10011992500",  # BRAMBLEWOOD, MAIN ROAD, LITTLE FRANSHAM, DEREHAM
                "10094466362",  # HEDGEROW, MAIN ROAD, LITTLE FRANSHAM, DEREHAM
                "10094466363",  # PARTRIDGE, MAIN ROAD, LITTLE FRANSHAM, DEREHAM
                "10094466365",  # OAKLANDS, MAIN ROAD, LITTLE FRANSHAM, DEREHAM
            ]
        ):
            return None

        if record.post_code in [
            # split
            "NR20 3JS",
            "NR17 1QJ",
            "NR19 2LT",
            "NR19 1PS",
            "NR19 1EU",
            "NR17 1JX",
            "NR20 3QB",
            "IP25 6HD",
            "IP25 6QX",
            "NR16 2AE",
            # suspect
            "PE37 7JP",  # SEA LORD CLOSE, SWAFFHAM
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # bugreport #627
        # coords change for: Dereham Town Football Club, Aldiss Park, Norwich Road, Dereham, NR20 3PX
        if record.polling_place_id == "13525":
            record = record._replace(
                polling_place_easting="601036", polling_place_northing="313508"
            )

        if record.polling_place_id in [
            "13658",  # Rocklands Village Hall The Street Rocklands
            "13745",  # Ovington Village Hall Church Road Ovington
            "13893",  # Oxborough Village Hall Swaffham Road Oxborough
        ]:
            # The E/N points are the wrong way round for these 3, perform the ol' switcheroo
            easting = record.polling_place_northing
            northing = record.polling_place_easting
            record = record._replace(polling_place_easting=easting)
            record = record._replace(polling_place_northing=northing)

        return super().station_record_to_dict(record)
