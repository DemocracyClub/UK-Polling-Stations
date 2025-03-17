from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SHR"
    addresses_name = (
        "2025-05-01/2025-03-17T10:15:03.781984/Democracy_Club__01May2025 2.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-17T10:15:03.781984/Democracy_Club__01May2025 2.tsv"
    )
    elections = ["2025-05-01"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # more accurate point for: Rhydycroesau Village Hall, Rhydycroesau, Oswestry, SY10 7PS
        if record.polling_place_id == "36230":
            record = record._replace(polling_place_easting=324197)
            record = record._replace(polling_place_northing=330779)

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10013136641",  # 11 HOLLINWOOD, WHIXALL, WHITCHURCH
                "10003419569",  # 2 GAGGS ROCK COTTAGE, QUATFORD, BRIDGNORTH
                "200003847491",  # 2 SILVINGTON HILL, HOPTON WAFERS, KIDDERMINSTER
                "10032917307",  # 12 THE TITRAIL, CLEE HILL, LUDLOW
                "10032918551",  # NANT ARGOED, ARGOED, CLUN, CRAVEN ARMS
                "10011839605",  # MEADOW CROFT, SNAILBEACH, SHREWSBURY
                "200001773022",  # SUNNYBANK, ROWTON, HALFWAY HOUSE, SHREWSBURY
                "100071219615",  # MOUNTAIN VIEW, WHIP LANE, KNOCKIN, OSWESTRY
                "10013134064",  # ASCOT HOUSE, ST. MARTINS, OSWESTRY
                "10013134670",  # RUE WOOD COTTAGE, RUE WOOD, WEM, SHREWSBURY
                "10002206313",  # SUNNYSIDE, COMLEY, LEEBOTWOOD, CHURCH STRETTON
                "10003419311",  # COPPICE FARM, HAUGHTON, BRIDGNORTH
                "10003417392",  # FIRS FARM, SHIRLETT, BROSELEY
                "10014526277",  # 67 SHIRLETT, BROSELEY
                "10094729404",  # THE CHAMBERS, THE INSTONES BUILDING, BRIDGNORTH ROAD, BROSELEY
                "10094729405",  # THE MERCHANTS, THE INSTONES BUILDING, BRIDGNORTH ROAD, BROSELEY
                "100071211852",  # CERDIC, HIGH STREET, BROSELEY
                "200003852192",  # ASTON HALL LODGE, ASTON ROAD, SHIFNAL
                "10013135347",  # GREEN LANE FARM, WHIXALL, WHITCHURCH
                "10014523638",  # YEW TREE HOUSE, WHIXALL, WHITCHURCH
                "200003849787",  # BEECHLEA, BROCKTON, MUCH WENLOCK
                "10007016042",  # SWISS COTTAGE, MORTON, OSWESTRY
                "100071220450",  # 1 CANONBURY, SHREWSBURY
                "10013135899",  # UPPER COLLEGE FARM, HIGHER HEATH, WHITCHURCH
                "10013134434",  # HOLLY BANK, FOXHOLES, WEM, SHREWSBURY
                "10032918552",  # ARGOED COTTAGE, ARGOED, CLUN, CRAVEN ARMS
            ]
        ):
            return None

        if record.addressline6 in [
            # splits
            "WV16 6QU",
            "SY2 6JT",
            "SY4 4EZ",
            "SY10 9FQ",
            "SY11 2LB",
            "SY5 9PE",
            "SY11 3LP",
            "TF9 3HE",
            "TF9 3HD",
            "TF13 6QA",
            "TF12 5SH",
            "SY13 1NE",
            "SY5 0PX",
            "SY6 7HQ",
            "TF11 9HX",
            "SY6 6HN",
            "TF11 8DN",
            "SY4 5JQ",
            "DY14 8QD",
            "SY8 3JY",
            "TF9 3RJ",
            "SY3 8RE",
            "SY11 4PX",
            # looks wrong
            "TF12 5BZ",
        ]:
            return None

        return super().address_record_to_dict(record)
