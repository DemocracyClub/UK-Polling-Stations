from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BRE"
    addresses_name = (
        "2023-05-04/2023-04-17T08:55:03.552669/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-17T08:55:03.552669/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100091495478",  # M LAMBERT PLANT LTD, MILL POND FARM, THETFORD ROAD, GARBOLDISHAM, DISS
            "10011976645",  # HAWTHORNS, BOTTLE CORNER, BESTHORPE, ATTLEBOROUGH
            "10011990571",  # THE SPINNEY, SCHOOL ROAD, BRISLEY, DEREHAM
            "10011967701",  # THE GRANARY, LING ROAD, NORTH LOPHAM, DISS
            "10011987611",  # BLACKWATER LAKE, SHADWELL, THETFORD
            "10011968735",  # THE BUNGALOW, MAIN ROAD, LITTLE FRANSHAM, DEREHAM
            "10094466364",  # BIRCHWOOD, MAIN ROAD, LITTLE FRANSHAM, DEREHAM
        ]:
            return None

        if record.post_code in [
            "NR19 1PS",
            "NR19 1EU",
            "NR17 1QJ",
            "NR17 1JX",
            "NR16 2AE",
            "NR19 2UJ",
            "NR19 2LT",
            "NR20 3QB",
            "IP25 6QX",
            "NR20 3JS",
            "IP24 1NB",  # MUNDFORD ROAD, THETFORD
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.polling_place_id in [
            "11430",  # Rocklands Village Hall The Street Rocklands
            "11660",  # Ovington Village Hall Church Road Ovington
            "11482",  # Oxborough Village Hall Swaffham Road Oxborough
        ]:
            # The E/N points are the wrong way round for these 3, perform the ol' switcheroo
            easting = record.polling_place_northing
            northing = record.polling_place_easting
            record = record._replace(polling_place_easting=easting)
            record = record._replace(polling_place_northing=northing)

        return super().station_record_to_dict(record)
