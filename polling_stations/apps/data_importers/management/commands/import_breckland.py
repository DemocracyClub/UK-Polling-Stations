from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BRE"
    addresses_name = "2024-05-02/2024-04-03T14:11:22.611445/Democracy_Club__02May2024_Breckland Council.tsv"
    stations_name = "2024-05-02/2024-04-03T14:11:22.611445/Democracy_Club__02May2024_Breckland Council.tsv"
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
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
        ]:
            return None

        if record.post_code in [
            # split
            "NR17 1JX",
            "IP25 6QX",
            "NR19 1PS",
            "NR19 1EU",
            "NR19 2LT",
            "NR20 3JS",
            "NR17 1QJ",
            "NR16 2AE",
            "IP25 6HD",
            "NR20 3QB",
            # suspect
            "PE37 7JP",  # SEA LORD CLOSE, SWAFFHAM
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.polling_place_id in [
            "12323",  # Rocklands Village Hall The Street Rocklands
            "12460",  # Ovington Village Hall Church Road Ovington
            "12581",  # Oxborough Village Hall Swaffham Road Oxborough
        ]:
            # The E/N points are the wrong way round for these 3, perform the ol' switcheroo
            easting = record.polling_place_northing
            northing = record.polling_place_easting
            record = record._replace(polling_place_easting=easting)
            record = record._replace(polling_place_northing=northing)

        return super().station_record_to_dict(record)
