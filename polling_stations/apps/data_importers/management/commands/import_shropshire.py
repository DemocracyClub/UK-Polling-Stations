from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SHR"
    addresses_name = (
        "2024-07-04/2024-06-07T13:35:57.112633/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-07T13:35:57.112633/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # more accurate point for: Rhydycroesau Village Hall, Rhydycroesau, Oswestry, SY10 7PS
        if record.polling_place_id == "35251":
            record = record._replace(polling_place_easting=324197)
            record = record._replace(polling_place_northing=330779)

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10094728399",  # CARAVAN AT STORAGE YARD ADJACENT THE FIRS HEATH ROAD, PREES HEATH, WHITCHURCH
            "10014529796",  # THE POPLARS, STEEL HEATH, WHITCHURCH
            "10013136641",  # 11 HOLLINWOOD, WHIXALL, WHITCHURCH
            "10014525628",  # BLUE WAGON, TERN HILL, MARKET DRAYTON
            "10013142887",  # SOWBATH BARN, MORETON MILL, SHAWBURY, SHREWSBURY
            "10014528560",  # HUSSEY FARM, BROAD OAK, SHREWSBURY
            "10002206666",  # ARLEY HOUSE, UFFINGTON, SHREWSBURY
            "200000127135",  # 1 LOWER LONGWOOD, EATON CONSTANTINE, SHREWSBURY
            "100071211848",  # 85A HIGH STREET, BROSELEY
            "200003849518",  # 5 OLD WORCESTER ROAD, ALBRIGHTON
            "100070011103",  # 3 BRINDLEY CLOSE, ALBRIGHTON, WOLVERHAMPTON
            "10003417373",  # BRAMBLE COTTAGE, LINLEY BROOK, BRIDGNORTH
            "10003419569",  # 2 GAGGS ROCK COTTAGE, QUATFORD, BRIDGNORTH
            "200003847491",  # 2 SILVINGTON HILL, HOPTON WAFERS, KIDDERMINSTER
            "10032917307",  # 12 THE TITRAIL, CLEE HILL, LUDLOW
            "10012073467",  # ELM FARM, FISHMORE, LUDLOW
            "10032918109",  # VERNOLDS COMMON CHAPEL RACECOURSE JUNCTION THE CLUB HOUSE TO NORTON JUNCTION ONIBURY ROAD, BROMFIELD
            "10093751437",  # LITTLE DUFFERYN, NEWCASTLE, CRAVEN ARMS
            "10032918551",  # NANT ARGOED, ARGOED, CLUN, CRAVEN ARMS
            "10011839605",  # MEADOW CROFT, SNAILBEACH, SHREWSBURY
            "10002207344",  # LITTLE LYTH BARN, LYTH HILL, BAYSTON HILL, SHREWSBURY
            "10014528855",  # BRAMBLE BARN, LYTH HILL, BAYSTON HILL, SHREWSBURY
            "10014533524",  # LIVING ACCOMMODATION THE VAULTS 16 CASTLE GATES, SHREWSBURY
            "100070050670",  # 2 MYTTON OAK ROAD, SHREWSBURY
            "200000126685",  # HEATH FARM, ROWTON, HALFWAY HOUSE, SHREWSBURY
            "200000126691",  # (CROCKETT), ROCK COTTAGE, ROWTON, HALFWAY HOUSE, SHREWSBURY
            "200001773022",  # SUNNYBANK, ROWTON, HALFWAY HOUSE, SHREWSBURY
            "10011839771",  # WALNUT COTTAGE, MARCHE LANE, HALFWAY HOUSE, SHREWSBURY
            "200000126817",  # SOMERDALE COTTAGE, WESTBURY, SHREWSBURY
            "100071219615",  # MOUNTAIN VIEW, WHIP LANE, KNOCKIN, OSWESTRY
            "10095708444",  # 2 CASSIDY DRIVE, GOBOWEN, OSWESTRY
            "10013134064",  # ASCOT HOUSE, ST. MARTINS, OSWESTRY
            "10013134670",  # RUE WOOD COTTAGE, RUE WOOD, WEM, SHREWSBURY
            "10014526022",  # DAIRY HOUSE, WEM LANE, SOULTON, WEM, SHREWSBURY
            "10002205022",  # THE STABLES, WALKMILLS, CHURCH STRETTON
            "10002206313",  # SUNNYSIDE, COMLEY, LEEBOTWOOD, CHURCH STRETTON
            "100071211618",  # 10 WESTGATE, BRIDGNORTH
            "200003849799",  # THE SHIELING, TASLEY, BRIDGNORTH
            "10003419311",  # COPPICE FARM, HAUGHTON, BRIDGNORTH
            "10003417392",  # FIRS FARM, SHIRLETT, BROSELEY
            "10014526277",  # 67 SHIRLETT, BROSELEY
            "10094729404",  # THE CHAMBERS, THE INSTONES BUILDING, BRIDGNORTH ROAD, BROSELEY
            "10094729405",  # THE MERCHANTS, THE INSTONES BUILDING, BRIDGNORTH ROAD, BROSELEY
            "100071211852",  # CERDIC, HIGH STREET, BROSELEY
            "200003852192",  # ASTON HALL LODGE, ASTON ROAD, SHIFNAL
            "10007023052",  # THE CROFT, BLODWEL BANK, TREFLACH, OSWESTRY
            "200001521617",  # 6A BEATRICE STREET, OSWESTRY
            "10013133473",  # BROOKLANDS, NEW MARTON, ST. MARTINS, OSWESTRY
            "10013135347",  # GREEN LANE FARM, WHIXALL, WHITCHURCH
            "10014523638",  # YEW TREE HOUSE, WHIXALL, WHITCHURCH
            "200003849787",  # BEECHLEA, BROCKTON, MUCH WENLOCK
            "200003845824",  # STONE COTTAGE, APLEY PARK, BRIDGNORTH
            "10007016042",  # SWISS COTTAGE, MORTON, OSWESTRY
            "100071220450",  # 1 CANONBURY, SHREWSBURY
        ]:
            return None

        if record.addressline6 in [
            # splits
            "SY1 2UG",
            "WV15 6BW",
            "SY10 9FQ",
            "TF9 3HD",
            "SY6 7HQ",
            "SY11 2LB",
            "TF12 5SH",
            "SY6 6HN",
            "TF9 3HE",
            "SY5 9PE",
            "SY4 5JQ",
            "SY11 4PX",
            "SY3 8RE",
            "TF11 8DN",
            "TF13 6QA",
            "SY5 0PX",
            "SY8 3JY",
            "SY11 3LP",
            "TF9 3RJ",
            # looks wrong
            "SY1 3PB",
            "WV16 4QQ",
            "TF12 5BZ",
            "TF11 9PG",
        ]:
            return None

        return super().address_record_to_dict(record)
