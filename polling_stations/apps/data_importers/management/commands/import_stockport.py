from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SKP"
    addresses_name = "2021-03-22T11:08:59.256823/Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-22T11:08:59.256823/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10002096787",  # FLAT TORKINGTON ROAD STABLES TORKINGTON ROAD, HAZEL GROVE, STOCKPORT
            "10093012711",  # 155A STOCKPORT ROAD, MARPLE, STOCKPORT
            "100011526060",  # 27 THE CLOUGH, STOCKPORT
            "100011526066",  # 33 THE CLOUGH, STOCKPORT
            "100011526058",  # 25 THE CLOUGH, STOCKPORT
            "100011526064",  # 31 THE CLOUGH, STOCKPORT
            "100011526056",  # 23 THE CLOUGH, STOCKPORT
            "100011526062",  # 29 THE CLOUGH, STOCKPORT
            "10002096735",  # 16B MARPLE ROAD, OFFERTON, STOCKPORT
            "100011432786",  # 6 DEMMINGS ROAD, CHEADLE
            "100011432788",  # 8 DEMMINGS ROAD, CHEADLE
        ]:
            return None

        if record.addressline6 in [
            "SK8 3TJ",
            "SK8 6BG",
            "SK8 3DQ",
            "SK6 2BD",
            "SK6 1AY",
            "SK6 1NL",
            "SK7 4NX",
            "SK7 4AJ",
            "SK7 4DF",
            "SK7 2AA",
            "SK6 6LP",
            "SK6 5NY",
            "SK6 6DF",
            "SK6 3BT",
            "SK7 3LZ",
            "SK6 4EN",
            "SK6 4HT",
            "SK6 1JG",
            "SK5 6XD",
            "SK5 7BJ",
            "SK4 5DA",
            "SK2 7HJ",
            "SK2 6LW",
            "SK6 7DH",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Kingsway School (Lower) Broadway Campus High Grove Road Cheadle SK8 1NP
        if record.polling_place_id == "10415":
            record = record._replace(polling_place_easting="")
            record = record._replace(polling_place_northing="")

        return super().station_record_to_dict(record)
