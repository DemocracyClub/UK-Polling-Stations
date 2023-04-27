from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ESK"
    addresses_name = "2023-05-04/2023-04-26T20:46:56.038428/East Suffolk Council - Democracy Club - Polling Districts May 2023.csv"
    stations_name = "2023-05-04/2023-04-26T20:46:56.038428/East Suffolk Council - Democracy Club - Polling Stations May 2023.csv"
    elections = ["2023-05-04"]

    def station_record_to_dict(self, record):
        # Loads of dodgy points
        if record.stationcode in [
            "S110",  # Dallinghoo Jubilee Hall
            "S138",  # Bruisyard Village Hall
            "S196",  # Fred Reynolds Centre
            "S195",  # Avenue Evangelical Church Hall
            "S159",  # Burness Parish Room
            "S184",  # Colneis Division Guiding HQ
            "S182",  # Christ Church
            "S187",  # Campsea Ashe Victory Hall
            "S160",  # Burness Parish Room
            "S141",  # Cransford Village Hall
            "S147",  # Great Glemham Village Hall
            "S109",  # Clopton Village Hall
            "S165",  # Kirton Church Hall
            "N69",  # Linstead Village Hall
        ]:
            record = record._replace(xordinate="", yordinate="")

        # Council said get rid of all of them...
        # List above left in for future reference
        record = record._replace(xordinate="", yordinate="")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.postcode in [
            "NR35 1BZ",  # split
        ]:
            return None

        return super().address_record_to_dict(record)
