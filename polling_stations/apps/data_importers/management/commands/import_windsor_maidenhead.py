from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "WNM"
    addresses_name = "2024-07-04/2024-06-20T15:27:14.770632/Democracy Club GE PD.csv"
    stations_name = (
        "2024-07-04/2024-06-20T15:27:14.770632/Democracy Club GE stations.csv"
    )
    elections = ["2024-07-04"]
    csv_encoding = "utf-16le"

    def station_record_to_dict(self, record):
        # A Mobile Unit at Waitrose Carpark, SL5 0HD
        if record.stationcode == "237WSC3":
            record = record._replace(xordinate="", yordinate="")

        if record.stationcode in (
            "150MBBN",
            "151MBBN",
            "152MBBS",
            "153MBBS",
            "154MBFW",
            "155MBFW",
            "156MBWC",
            "157MIAP-MISF",
            "158MICR",
            "159MINA",
            "160MINA",
            "161MIWI",
            "162MWWE",
            "163MWSM",
            "164MWWP",
            "240CPA",
            "241CPB",
            "242CPB",
            "243CPC",
            "244LAA",
            "245LAB",
            "246LFA",
            "247LFB",
            "248LSC",
            "250EGE1",
            "251EGE2",
            "252EGW1",
            "253EGW1",
            "254VW1",
            "255VW2-VW4",
            "256VW3",
        ):
            return None

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.postcode in [
            "KW15 1WU",
        ]:
            return None
        return super().address_record_to_dict(record)
