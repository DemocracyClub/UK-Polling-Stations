from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "SLK"
    addresses_name = "2026-05-07/2026-03-17T15:16:09.979745/Democracy Club - Idox_2026-03-17 14-23.csv"
    stations_name = "2026-05-07/2026-03-17T15:16:09.979745/Democracy Club - Idox_2026-03-17 14-23.csv"
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        if record.uprn in [
            "484131230",  # MUIRHOUSE FARM, THANKERTON, BIGGAR, ML12 6NJ
            "484140163",  # WOODLEA, THANKERTON, BIGGAR, ML12 6NF
            "484121979",  # BROOKFIELD, DEVONSIDE ROAD, CARMICHAEL, BIGGAR, ML12 6PQ
            "484180542",  # SEAFORTH COURTYARD, BRAIDWOOD, CARLUKE, ML8 5NE
            "484114775",  # HAWTHORN COTTAGE CARTLAND BRIDGE, LANARK, ML11 9UF
            "484017180",  # 184 GLENFRUIN ROAD, BLANTYRE, GLASGOW, G72 9RL
            "484011788",  # BARONHILL, HUNTHILL ROAD, BLANTYRE, GLASGOW, G72 9UY
        ]:
            return None

        if record.postcode in [
            # split
            "G74 4DF",
            "G72 8WN",
            "ML3 9GD",
            "G72 8FG",
            "G72 7NT",
            "ML11 0PG",
            "G75 8JW",
            "G73 4AP",
            "G72 7XQ",
            "ML10 6ET",
            "ML11 0BG",
            "G75 8ND",
            "ML12 6PP",
            "ML10 6FB",
            "ML12 6SW",
            # looks wrong
            "ML12 6JJ",
        ]:
            return None

        return super().address_record_to_dict(record)
