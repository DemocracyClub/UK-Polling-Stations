from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BRX"
    addresses_name = "2022-05-05/2022-03-10T15:48:58.245362/Democracy Club - Polling Districts 2022 Borough of Broxbourne.csv"
    stations_name = "2022-05-05/2022-03-10T15:48:58.245362/Democracy Club - Polling Stations 2022 Borough of Broxbourne.csv"
    elections = ["2022-05-05"]

    def station_record_to_dict(self, record):

        # FAIRFIELDS PRIMARY  SCHOOL, (LITTLE FIELDS PRE SCHOOL)
        if record.stationcode == "23":
            record = record._replace(xordinate="534213")
            record = record._replace(yordinate="203580")

        # FLAMSTEAD END HALL, MAYO CLOSE
        if record.stationcode == "22":
            record = record._replace(xordinate="535062")
            record = record._replace(yordinate="203335")

        # FAIRLEY CROSS HALL, ROSEDALE COMMUNITY CHURCH
        if record.stationcode == "27":
            record = record._replace(xordinate="534455")
            record = record._replace(yordinate="203051")

        # HALSEY HALL, TURNERS HILL
        if record.stationcode in ["16", "17", "17A"]:
            record = record._replace(xordinate="535906")
            record = record._replace(yordinate="201922")

        # CHRIST CHURCH, CHURCH HALL, TRINITY LANE, WALTHAM CROSS, EN8 7ED
        if record.stationcode == "18":
            record = record._replace(xordinate="535999")
            record = record._replace(yordinate="201098")

        return super().station_record_to_dict(record)
