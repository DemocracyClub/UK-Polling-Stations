from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "PKN"
    addresses_name = "2026-05-07/2026-03-16T14:56:55.682559/Democracy Club - Idox_2026-03-16 14-31.csv"
    stations_name = "2026-05-07/2026-03-16T14:56:55.682559/Democracy Club - Idox_2026-03-16 14-31.csv"
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        if (
            record.uprn
            in [
                "124064151",  # ALLERBURN BLACKCRAIG A924 FROM MAIN ROAD TO THE ACCESS ROAD AT CALLY LODGE, BALLINTUIM
                "124093529",  # SOUTH LOCHTON HOUSE, ABERNYTE, PERTH
                "124065025",  # GLENBRAN FARM, ABERNYTE, PERTH
                "124061546",  # GLENFARG HOUSE, GLENFARG, PERTH
                "124115777",  # ARCHSTONE HOUSE, CLEISH, KINROSS
                "124064294",  # LITTLERIGG, DUNNING GLEN, DOLLAR
                "124075288",  # BRACKETRIGGS, CRIEFF
            ]
        ):
            return None

        if record.postcode in [
            # split
            "PH3 1HD",
            "PH10 6TD",
            "PH2 9BH",
            "PH1 2RH",
            "PH14 9SY",
            "PH11 8NF",
            # looks wrong
            "KY13 9LY",
            "PH14 9SU",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # provided by the council
        # Postcode correction for: Carse of Gowrie Kirk - Invergowrie, 1 Errol Road, Invergowrie, DD1 5AD
        if record.pollingstationnumber == "42":
            record = record._replace(pollingstationpostcode="DD2 5AD")

        # Postcode correction for: Milnathort Town Hall, 1 New Road, Milnathort, Kinross, KY13 8XT
        if record.pollingstationnumber in ["100", "101"]:
            record = record._replace(pollingstationpostcode="KY13 9XT")

        # Postcode correction for: Aberfeldy Town Hall, Crieff Road, Aberfeldy, Perthshire, PH15 2DU
        if record.pollingstationnumber == "25":
            record = record._replace(pollingstationpostcode="PH15 2BJ")

        # Postcode correction for: Dunning Parish Church, Perth Road, Dunning, Perth, PH2 0QD
        if record.pollingstationnumber == "99":
            record = record._replace(pollingstationpostcode="PH2 0RY")

        return super().station_record_to_dict(record)
