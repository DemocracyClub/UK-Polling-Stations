from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BRE"
    addresses_name = "2021-04-07T16:45:08.424818/Democracy_Club__06May2021.tsv"
    stations_name = "2021-04-07T16:45:08.424818/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        if record.polling_place_id in [
            "10265",  # Rocklands Village Hall The Street Rocklands
            "10216",  # Ovington Village Hall Church Road Ovington
            "10163",  # Oxborough Village Hall Swaffham Road Oxborough
        ]:
            # The E/N points are the wrong way round for these 3
            # perform the ol' switcheroo
            easting = record.polling_place_northing
            northing = record.polling_place_easting
            record = record._replace(polling_place_easting=easting)
            record = record._replace(polling_place_northing=northing)

        # Dereham Town Football Club Aldiss Park Norwich Road, Dereham
        if record.polling_place_id == "9911":
            record = record._replace(polling_place_easting="601038")
            record = record._replace(polling_place_northing="313511")

        # The Red Lion East Church Street Kenninghall NR16 2EP
        if record.polling_place_id == "9996":
            record = record._replace(polling_place_easting="")
            record = record._replace(polling_place_northing="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100091495478",  # M LAMBERT PLANT LTD, MILL POND FARM, THETFORD ROAD, GARBOLDISHAM, DISS
            "10011976645",  # HAWTHORNS, BOTTLE CORNER, BESTHORPE, ATTLEBOROUGH
            "10011993736",  # 1A SCARNING FEN, DEREHAM
            "10011990571",  # THE SPINNEY, SCHOOL ROAD, BRISLEY, DEREHAM
        ]:
            return None

        if record.post_code in [
            "IP25 6TF",
            "IP25 7BS",
            "IP24 2JJ",
            "IP25 2JB",
            "IP25 6XY",
            "IP25 6YU",
            "PE37 7JP",
        ]:
            return None

        return super().address_record_to_dict(record)
