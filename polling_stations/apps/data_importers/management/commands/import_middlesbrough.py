from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MDB"
    addresses_name = "2021-03-19T13:12:12.661477/Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-19T13:12:12.661477/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10023174603",  # 38 RAVENDALE ROAD, MIDDLESBROUGH
            "10023181141",  # 34 RAVENDALE ROAD, MIDDLESBROUGH
            "10023181142",  # 32 RAVENDALE ROAD, MIDDLESBROUGH
            "200000259465",  # 21B ST. BARNABAS ROAD, MIDDLESBROUGH
            "10023174667",  # 36 RAVENDALE ROAD, MIDDLESBROUGH
            "200001683756",  # 220A LINTHORPE ROAD, MIDDLESBROUGH
            "10023181276",  # THE GRANARY, STAINSBY HALL FARM, THORNABY, STOCKTON-ON-TEES
            "100110131624",  # FLAT CAPTAIN COOK HOTEL 7-11 DURHAM STREET, MIDDLESBROUGH
            "100110131626",  # 21C ST. BARNABAS ROAD, MIDDLESBROUGH
            "100110131622",  # FLAT 1 169 BOROUGH ROAD, MIDDLESBROUGH
            "10023181264",  # FLAT 1 168 LINTHORPE ROAD, MIDDLESBROUGH
            "10023172775",  # GRANGE LODGE, HEMLINGTON LANE, HEMLINGTON, MIDDLESBROUGH
            "100110791007",  # GRANGE HOUSE, HEMLINGTON LANE, HEMLINGTON, MIDDLESBROUGH
            "10093978033",  # FLAT 1 TOBY CARVERY MARTON ROAD, MIDDLESBROUGH
            "10023181033",  # GROUND FLOOR 82 BOROUGH ROAD, MIDDLESBROUGH
            "10023181034",  # FIRST FLOOR 82 BOROUGH ROAD, MIDDLESBROUGH
        ]:
            return None

        if record.addressline6 in ["TS1 3QD", "TS1 2ET", "TS5 5EG", "TS1 4AD"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Memorial Hall Meldyke Lane Stainton Middlesbrough TS8 9AU
        if record.polling_place_id == "9056":
            record = record._replace(polling_place_easting="448034")
            record = record._replace(polling_place_northing="514186")

        # Marton Manor Primary School The Derby Middlesbrough TS7 8RH
        if record.polling_place_id == "9044":
            record = record._replace(polling_place_easting="451145")
            record = record._replace(polling_place_northing="515806")

        # ACTES Resource Centre Meath Street Middlesbrough TS1 4RY
        if record.polling_place_id == "8923":
            record = record._replace(polling_place_easting="448379")
            record = record._replace(polling_place_northing="519367")

        # Linthorpe Community School Roman Road Linthorpe Middlesbrough TS5 6EA
        if record.polling_place_id == "8948":
            record = record._replace(polling_place_easting="448699")
            record = record._replace(polling_place_northing="518439")

        return super().station_record_to_dict(record)
