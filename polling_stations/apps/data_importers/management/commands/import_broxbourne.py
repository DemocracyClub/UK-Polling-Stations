from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BRX"
    addresses_name = "2021-03-19T10:23:06.876474/Democracy club - polling districts 2021 Borough of Broxbourne.csv"
    stations_name = "2021-03-19T10:23:06.876474/Democracy club - polling stations 2021 Borough of Broxbourne.csv"
    elections = ["2021-05-06"]

    def station_record_to_dict(self, record):

        # Fairfields primary school
        if record.stationcode in ["14A", "14"]:
            record = record._replace(xordinate="534213")
            record = record._replace(yordinate="203580")

        # Flamstead End Hall
        if record.stationcode in ["22", "22A"]:
            record = record._replace(xordinate="535062")
            record = record._replace(yordinate="203335")

        # Fairley Cross Hall, Rosedale Community Church
        if record.stationcode in ["31", "16"]:
            record = record._replace(xordinate="534455")
            record = record._replace(yordinate="203051")

        # HALSEY HALL
        if record.stationcode in ["23", "23A", "21", "21A"]:
            record = record._replace(xordinate="535906")
            record = record._replace(yordinate="201922")

        # Christ Church, Church Hall, Trinity Lane, Waltham Cross, EN8 7ED
        if record.stationcode == "24":
            record = record._replace(xordinate="535999")
            record = record._replace(yordinate="201098")

        # Hurst Drive Primary School, Hurst Drive, Waltham Cross EN8 8DH
        if record.stationcode == "25":
            record = record._replace(xordinate="535576")
            record = record._replace(yordinate="200249")

        return super().station_record_to_dict(record)
