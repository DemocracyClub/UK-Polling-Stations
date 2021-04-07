from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SHR"
    addresses_name = (
        "2021-03-22T10:30:15.417602/Shropshire Democracy_Club__06May2021.tsv"
    )
    stations_name = (
        "2021-03-22T10:30:15.417602/Shropshire Democracy_Club__06May2021.tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        # Stanton Lacy Village Hall, Stanton Lacy, Ludlow
        if record.polling_place_id == "28379":
            record = record._replace(polling_place_easting="352573")
            record = record._replace(polling_place_northing="280557")
            record = record._replace(polling_place_postcode="")

        # Farlow & Oreton Village Hall, Fox Hill, Oreton, Kidderminster, Worcs
        if record.polling_place_id == "28018":
            record = record._replace(polling_place_easting="364411")
            record = record._replace(polling_place_northing="280033")

        # Nesscliffe Village Hall, Nesscliffe, Shrewsbury
        if record.polling_place_id == "28037":
            record = record._replace(
                polling_place_postcode="SY4 1AX", polling_place_uprn="10011838276"
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10014525628",  # BLUE WAGON, TERN HILL, MARKET DRAYTON
            "10014529796",  # THE POPLARS, STEEL HEATH, WHITCHURCH
            "10013136897",  # LOWE COTTAGE FARM, THE LOWE, WEM, SHREWSBURY
            "10014526022",  # DAIRY HOUSE, WEM LANE, SOULTON, WEM, SHREWSBURY
            "10013142887",  # SOWBATH BARN, MORETON MILL, SHAWBURY, SHREWSBURY
            "10013135195",  # THE DRUMBLES, RUYTON ROAD, BASCHURCH, SHREWSBURY
            "200000126685",  # HEATH FARM, ROWTON, HALFWAY HOUSE, SHREWSBURY
            "10014543870",  # NEW BUNGALOW, ROWTON, HALFWAY HOUSE, SHREWSBURY
            "200001773027",  # ROWTON GRANGE, ROWTON, HALFWAY HOUSE, SHREWSBURY
            "200001672845",  # LOWER HOUSE FARM, KNOCKIN, OSWESTRY
            "10007023052",  # THE CROFT BLODWEL BANK, TREFLACH
            "10007022014",  # 96 WELSH WALLS, OSWESTRY
            "10014528648",  # FLAT, 105 LONGDEN ROAD, SHREWSBURY
            "10014546849",  # 2 WHITE LODGE, THE MOUNT, SHREWSBURY
            "10014546848",  # 1 WHITE LODGE, THE MOUNT, SHREWSBURY
            "200000123118",  # BLYTH COTTAGE, SHELTON, SHREWSBURY
            "100071222901",  # SHELTON COTTAGE, THE MOUNT, SHELTON, SHREWSBURY
            "10002206666",  # ARLEY HOUSE, UFFINGTON, SHREWSBURY
            "10014528855",  # BRAMBLE BARN, LYTH HILL, BAYSTON HILL, SHREWSBURY
            "10002207344",  # LITTLE LYTH BARN, LYTH HILL, BAYSTON HILL, SHREWSBURY
            "10032918109",  # VERNOLDS COMMON CHAPEL RACECOURSE JUNCTION THE CLUB HOUSE TO NORTON JUNCTION ONIBURY ROAD, HIGH WALTON
            "10012073467",  # ELM FARM, FISHMORE, LUDLOW
            "10094729773",  # LIVING ACCOMMODATION AT 3 BULL RING, LUDLOW
            "10014543541",  # SWALLOWS BARN, COOMBE FARM, STOTTESDON, KIDDERMINSTER
            "200003849799",  # THE SHIELING, TASLEY, BRIDGNORTH
            "10014546730",  # 1 THE HAWTHORNS ALBRIGHTON BY-PASS, ALBRIGHTON
            "200003849518",  # 5 OLD WORCESTER ROAD, ALBRIGHTON
            "100071210835",  # OAKLANDS CHAPEL ROAD, ALVELEY
            "10007015422",  # LINDISFARNE, MAESBROOK, OSWESTRY
            "10070436337",  # FLAT RESTAURANT AND PREMISES A442 FROM LODGE FARM TO CHAPEL LANE QUATFORD, QUATFORD, BRIDGNORTH
        ]:
            return None

        if record.addressline6 in [
            "WV16 5EE",
            "SY5 6QP",
            "TF11 9PS",
            "TF11 9JL",
            "SY4 3JB",
            "SY4 3AE",
            "SY6 6HN",
            "SY6 7HQ",
            "SY4 5JQ",
            "SY11 4PX",
            "SY10 9EG",
            "SY22 6LG",
            "SY4 4SR",
            "DY14 0AH",
            "DY14 8EF",
            "WV16 6QU",
            "SY11 2LB",
            "TF9 2AD",
            "SY10 9HH",
            "TF9 3HD",
            "TF9 3HE",
            "SY11 3HR",
            "SY4 4SN",
            "SY2 5BP",
            "TF12 5BN",
            "SY3 8RE",
            "SY5 8JD",
            "SY12 9EU",
            "TF9 3RJ",
            "SY11 3EL",
            "SY11 1BB",
            "TF8 7JF",
            "SY11 3LP",
            "SY11 3JL",
            "SY11 3JP",
            "SY4 4EZ",
            "SY4 4NB",
            "SY4 4BE",
            "SY8 3JY",
            "SY3 8UG",
            "SY5 9PE",
            "SY5 0HJ",
            "SY6 7JS",
            "SY2 6QT",
            "TF11 8DN",
            "SY5 0PX",
            "SY1 2PE",
            "SY3 7JD",
            "SY3 7NR",
            "SY5 8BU",
            "WV16 4QQ",
        ]:
            return None

        return super().address_record_to_dict(record)
