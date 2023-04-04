from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BRX"
    addresses_name = "2023-05-04/2023-04-04T11:13:30.818764/Democracy club - 2nd attempt - polling districts 4-5-2023.csv"
    stations_name = "2023-05-04/2023-04-04T11:13:30.818764/Democracy Club - 2nd attempt - polling stations 4-5-2023.csv"
    elections = ["2023-05-04"]

    def station_record_to_dict(self, record):
        # FAIRFIELDS PRIMARY  SCHOOL, (LITTLE FIELDS PRE SCHOOL)
        if record.stationcode in ("23", "24"):
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

    def address_record_to_dict(self, record):
        uprn = record.uprn.lstrip("0").strip()

        if uprn in [
            "148043016",  # 11 ABINGDON COURT, HIGH STREET, WALTHAM CROSS
        ]:
            return None

        return super().address_record_to_dict(record)
