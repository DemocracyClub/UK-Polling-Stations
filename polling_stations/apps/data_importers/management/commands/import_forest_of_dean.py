from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "FOE"
    addresses_name = (
        "2025-05-01/2025-03-18T10:21:20.040469/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-18T10:21:20.040469/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if (
            record.property_urn
            in [
                "10090651915",  # THE PADDOCKS, NEWLAND, COLEFORD
                "10014327870",  # DUNFIGHTIN, PINGRY LANE, COLEFORD
                "10008092880",  # FRUIT TREES, PRINCE CRESCENT, STAUNTON, GLOUCESTER
                "10003812140",  # 38 BOUNDARY PLACE, CORSE, GLOUCESTER
                "10003816900",  # ANNETTES, BLACKWELLS END, HARTPURY, GLOUCESTER
                "10008094115",  # DURBRIDGE MILL, REDMARLEY, GLOUCESTER
                "10012752491",  # THE OLD CHAPEL, FOUR OAKS, NEWENT
                "10012751325",  # WOODSIDE, KEMPLEY ROAD, GORSLEY, ROSS-ON-WYE
                "10012751215",  # THE NEST, KEWS LANE, KILCOT, NEWENT
                "10014327797",  # KEWS BARN, KEWS LANE, KILCOT, NEWENT
                "10012751213",  # KEWS FARM, KEWS LANE, KILCOT, NEWENT
                "100120457399",  # 4 COOKS PLACE, HIGH STREET, NEWENT
                "100120457400",  # 5 COOKS PLACE, HIGH STREET, NEWENT
                "100121244390",  # IVY COTTAGE, LAKESIDE, NEWENT
                "10014328010",  # LITTLE ELMBRIDGE, STERRYS LANE, MAY HILL, LONGHOPE
                "100120454777",  # IVYBROOK COTTAGE, GANDERS GREEN, MAY HILL, LONGHOPE
                "10012936919",  # THE STABLES, BLAISDON, LONGHOPE
                "10014327448",  # BRACELANDS FARM HOUSE BRACELAND, CHRISTCHURCH
                "10012935681",  # WYESEAL FARM, LOWER WYE VALLEY ROAD, ST. BRIAVELS, LYDNEY
                "10008089531",  # THE COTTAGE CHERRY ORCHARD FARM ROAD FROM SWANPOOL WOOD TO JUNCTION WITH ALMHOUSE ROAD, NEWLAND
                "10008089532",  # CHERRY ORCHARD FARM, NEWLAND, COLEFORD
                "10008094492",  # THE CALF HOUSE, CHERRY ORCHARD FARM, NEWLAND, COLEFORD
                "100120452435",  # YEW TREE COTTAGE, MILL END, COLEFORD
                "10096000300",  # LOWER PERRYGROVE FARM, PINGRY LANE, COLEFORD
                "100121383612",  # OAKLEY LODGE, CASTLE VIEW COURT, BEACHLEY ROAD, TUTSHILL, CHEPSTOW
                "100120450982",  # NEWBURY HOUSE, CASTLE VIEW COURT, BEACHLEY ROAD, TUTSHILL, CHEPSTOW
                "10012934606",  # BRYANS, TIDENHAM, CHEPSTOW
                "10090650931",  # THE BRYANS FLAT A48 FROM JUNCTION WITH HANLEY LANE TO JUNCTION WITH GLOUCESTER ROAD, TIDENHAM
                "100121242286",  # 17 LOWER COMMON, AYLBURTON, LYDNEY
                "10008090256",  # FLAT, PARK FARMHOUSE, LYDNEY PARK ESTATE, LYDNEY
                "10090651182",  # STUDIO FLAT, PARK FARMHOUSE, LYDNEY PARK ESTATE, LYDNEY
                "10012752044",  # AYLEFORD COTTAGE, TWO BRIDGES, BLAKENEY
                "10012934339",  # SPRINGBANK, NEW ROAD, FLAXLEY, NEWNHAM
                "100121244668",  # WOODLANDS, HUNTLEY ROAD, TIBBERTON, GLOUCESTER
                "10003815614",  # BRAMBLE COTTAGE, CLEMENTS END, COLEFORD
                "10090650650",  # CLIMPERS, CLEMENTS END, COLEFORD
                "100120452431",  # KENNEL FARM, MILL END, COLEFORD
                "100120452429",  # KENNEL BARN, MILL END, COLEFORD
                "10003812478",  # CRAGLANDS, BLAIZE BAILEY, LITTLEDEAN, CINDERFORD
                "10012934888",  # TIBBS CROSS FARM, TIBBS CROSS, LITTLEDEAN, CINDERFORD
                "100120454263",  # FAWLEY VILLA, NEWENT LANE, HUNTLEY, GLOUCESTER
                "100120451744",  # KENSLEY LODGE, SPEECH HOUSE, COLEFORD
                "10012936428",  # BLUE BELLS, FOREST RISE, CINDERFORD
                "10012936427",  # BRAMBLES, FOREST RISE, CINDERFORD
                "10012936429",  # NIRVANA, FOREST RISE, CINDERFORD
                "100120456829",  # SHAPRIDGE COTTAGE, LOWER SHAPRIDGE, MITCHELDEAN
                "100121243363",  # ROCK HAVEN, CHURCH LANE, ABENHALL, MITCHELDEAN
                "100120452337",  # WOOLCOTT, LORDS HILL, COLEFORD
            ]
        ):
            return None

        if record.addressline6 in [
            # splits
            "GL14 2HQ",
            "GL17 9QU",
            "GL15 4AN",
            "GL14 2BB",
            "GL17 9JS",
            "GL18 1LN",
            # looks wrong
            "GL16 7ES",
            "GL15 5HD",
            "GL14 2BL",
            "GL14 2BN",
            "GL14 2FA",
            "GL14 2BU",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # easting correction for: Rudford & Highleadon Village Hall, Buttermilk Lane, Rudford, GL2 8DY
        if record.polling_place_id == "4192":
            record = record._replace(polling_place_easting="377237")

        # point correction for: Primrose Hill Church Hall, Primrose Hill, Lydney GL15 5SF
        if record.polling_place_id == "4116":
            record = record._replace(polling_place_easting="363533")
            record = record._replace(polling_place_northing="204434")

        return super().station_record_to_dict(record)
