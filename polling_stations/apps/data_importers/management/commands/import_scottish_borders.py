from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "SCB"
    addresses_name = "2021-03-25T12:10:21.663474/Democracy Club Polling Districts.csv"
    stations_name = "2021-03-25T12:10:21.663474/Democracy Club Polling Places.csv"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def station_record_to_dict(self, record):

        # MANOR VILLAGE HALL KIRKTON MANOR PEEBLES EH45 7JH
        if record.stationcode == "MAN009_1":
            record = record._replace(postcode="EH45 9JH")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "116063492",  # SCHIEHALLION, FAIRSLACKS, WEST LINTON
            "116065851",  # MOYHALL, PEEBLES
            "116090401",  # CARAVAN, BLACKADDER WEST, DUNS
            "116057743",  # WESTER FODDERLIE FARM HOUSE, HAWICK
            "116076251",  # SWINDON COTTAGE, KELSO
            "116062823",  # 26 LAMBERTON HOLDING, LAMBERTON, BERWICK-UPON-TWEED
            "116069378",  # GLEN BANK, GREENLAW, DUNS
            "116069690",  # BURNDEN, OXTON, LAUDER
            "116050796",  # CLOVERHILL HOUSE, FISHWICK MAINS, BERWICK-UPON-TWEED
            "116060667",  # CLIFFHOPE HOUSE, NEWCASTLETON
            "116057744",  # SCLATERFORD COTTAGE, WESTER FODDERLIE, HAWICK
            "116056643",  # FASTHEUGH, SELKIRK
            "116055268",  # THE BUNGALOW, MERSINGTON, GREENLAW, DUNS
            "116055919",  # SILVER BIRCHES, BLACKLEE, HAWICK
            "116053308",  # DREVA MUIRBURN, BROUGHTON, BIGGAR
            "116051442",  # WHEATHAUGH FARM COTTAGE, NEWCASTLETON
            "116064287",  # WHITEHALL WEST LODGE, DUNS
            "116065911",  # KIDSTON MILL, PEEBLES
            "116055916",  # BLACKLEE U67-3 U66-3 AT FORKINS TO B6357 AT CLEUGHHEAD, BONCHESTER BRIDGE
            "116055981",  # 5 HASSENDEAN FARM COTTAGES, HAWICK
            "116062629",  # GAMEKEEPERS COTTAGE, MAKERSTOUN, KELSO
            "116084513",  # 1 DUNS WYND, KELSO
            "116058818",  # ELBA, DUNS
            "116054751",  # BURNSIDE COTTAGE, COLDINGHAM MOOR, EYEMOUTH
            "116053328",  # DREVA CRAIG, BROUGHTON, BIGGAR
            "116053457",  # HIGHFIELD LODGE, AUCHENCROW, EYEMOUTH
            "116061121",  # LEA BANK HOUSE, HOARDWEEL FARM, DUNS
            "116056046",  # NORTH LODGE, WOLFLEE, HAWICK
            "116074488",  # GALLOWS LAW, EYEMOUTH
            "116056047",  # WOODLAND COTTAGE, WOLFLEE, HAWICK
            "116051546",  # THE STEEL, NINE MILE BURN, PENICUIK
            "116062611",  # GOSHIELAW, BELMONT, KELSO
        ]:
            return None

        if record.postcode in [
            "TD5 8PT",
            "TD1 1NS",
            "TD1 3NY",
            "TD11 3QE",
            "EH45 9JJ",
            "TD12 4LG",
            "TD11 3QL",
        ]:
            return None

        return super().address_record_to_dict(record)
